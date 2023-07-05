import os
import re
from dateutil.relativedelta import relativedelta

import pandas as pd
import tqdm

from .utils import get_header_indices, iter_reports


class RadParser:
    def __init__(self, rad_fp=None, clb_fp=None, dem_fp=None, pairs=None, debug=False):
        self.rad_fp = rad_fp
        self.clb_fp = clb_fp
        self.dem_fp = dem_fp
        self.pairs = pairs
        self.debug = debug

        self.rad_df = None
        self.clb_df = None
        self.dem_df = None

    def are_files_ready(self):
        """Basic validation that filepaths are set and exist.
        """
        ready = [
            fp is not None and os.path.exists(fp)
            for fp in [self.rad_fp, self.clb_fp, self.dem_fp]
        ]

        return all(ready)  # True if all filepaths are valid

    def get_rad_text(self, report):
        """Parses out raw radiology report findings with spaces stripped from the tails of every line.
        """
        rep = [line.strip(' ') for line in report]

        left = 0
        right = len(rep)
        for i in range(len(rep)):
            rep[i] = re.sub(r' +', ' ', rep[i])

            if left == 0 and 'FINDINGS' in rep[i]:
                left = i

            # removes text block that explains the PI-RADS levels
            if rep[i].startswith('PI-RADS 1') and ('highly unlikely' in rep[i].lower() or 'very low' in rep[i].lower()):
                right = i

        return ''.join(rep[left:right])

    def extract_accession_number(self, report):
        """Parses out accession number/exam number.
        """
        rep = [line.strip(' ') for line in report]

        pattern = re.compile(r'Exam Number:\s+([A-Z0-9]+)')
        acc_num = None
        for line in rep:
            if 'Exam Number' in line:
                search = re.search(pattern, line)

                if search is not None:
                    acc_num = search.group(1)

                break

        return acc_num

    def extract_pirads(self, report):
        """Parses out highest PI-RADS score."""
        pattern = re.compile(r'pi-rads\s?(score)?.*?(\d)')

        max_pirads = 0

        matches = re.findall(pattern, report.lower())
        if matches is None:
            return None
        else:
            for _, score in matches:
                max_pirads = max(int(score), max_pirads)

            if max_pirads == 0:
                return None
            else:
                return str(max_pirads)

    def extract_prostate_volume(self, report):
        """Parses out prostate volume."""
        pvol_line = ''
        for line in report.split('\n\n'):
            if "including 3+4 or 4+3 and/or volume > 0.5cc" in line:  # special note to ignore
                continue

            line = line.lower()

            if 'prostate' in line:
                if pvol_line != '':
                    pvol_line += ' '

                pvol_line += line

        if pvol_line == '':
            return None

        # print(pvol_line)

        cube_pattern = r'\(\s?(\d+(\.\d+)?).*?(x|by)\s?(\d+(\.\d+)?).*?(x|by)\s?(\d+(\.\d+)?).*?\)'  # i.e. (1.0 x 1.0 x 1.0)
        searches = [
            r'(\d+(\.\d+)?)\s?' + cube_pattern + r'\s?\/\s?2.*?cubic cm',  # i.e. 1.0 (1.0 x 1.0 x 1.0)/2 cubic cm
            cube_pattern + r'\s?\/\s?2.*?cubic cm',  # i.e. (1.1 x 1.1 x 1.1)/2 cubic cm
            cube_pattern + r'\s?\/\s?2.*?cubic cm',  # i.e. (1.1 x 1.1 x 1.1)/2 cubic cm
            r'=\s?(\d+(.\d+)?)\s?(cubic cm|ml|cc)',  # i.e. = 20 cubic cm | = 20 ml | = 20 cc
            r'(\d+(\.\d+)?)\s?(cubic cm|cc|ml)'  # i.e. 10 cubic cm | 10 cc | 10 ml
        ]

        pvol = None
        for i, pattern in enumerate(searches):
            search = re.search(pattern, pvol_line)

            if search is None:
                continue
            elif i in [0, 3, 4]:
                pvol = round(float(search.group(1)), 2)
            elif i in [1, 2]:
                v1 = float(search.group(1))
                v2 = float(search.group(4))
                v3 = float(search.group(7))

                pvol = round(v1 * v2 * v3 / 2, 1)

            break

        if pvol is not None:
            return str(pvol)
        else:
            return pvol

    def extract_rep_data(self, empi, date, report):
        rep = self.get_rad_text(report)
        acc = self.extract_accession_number(report)
        score = self.extract_pirads(rep)
        volume = self.extract_prostate_volume(rep)
        psa = None
        race = None
        birthday = None
        age = None

        clb = self.clb_df[(self.clb_df['EMPI'] == empi) & (self.clb_df['Seq_Date_Time'] < date)].dropna(
            subset=['Result'])
        num_mask = [re.match(r'^-?\d+(?:\.\d+)$', s) is not None for s in clb['Result']]
        clb = clb[num_mask]
        if len(clb) > 0:
            psa = clb[clb['Seq_Date_Time'] == clb['Seq_Date_Time'].max()]['Result'].values[0]

        dem = self.dem_df[self.dem_df['EMPI'] == empi]
        if len(dem) > 0:
            race = dem['Race'].values[0]
            birthday = pd.to_datetime(dem['Date_of_Birth'].values[0])
            age = relativedelta(date, birthday).years

        return [acc, score, volume, psa, race, age]

    def build_dfs(self):
        if not self.are_files_ready():
            raise RuntimeError("Radiology filepaths invalid/not set")

        self.dem_df = pd.read_csv(self.dem_fp, delimiter='|', dtype={'EMPI': str, 'MRN': str})

        self.clb_df = pd.read_csv(self.clb_fp, delimiter='|', dtype={'EMPI': str, 'MRN': str})
        self.clb_df['Seq_Date_Time'] = pd.to_datetime(self.clb_df['Seq_Date_Time'])

        rad_dict = {}  # i: [MRN, Date(of report), PI-RADS, prostate volume, PSA, race, birth date, age(during report)]
        with open(self.rad_fp) as rf:
            header_i = get_header_indices(rf.readline())

            for i, report in enumerate(tqdm.tqdm(iter_reports(rf))):
                header = report[0].split('|')
                mrn = header[header_i['MRN']]  # default identifier
                empi = header[header_i['EMPI']]  # more reliable for cross-table joins
                date = pd.to_datetime(header[header_i['Report_Date_Time']])
                pair = (mrn, date.strftime("%-m/%-d/%y"))

                if 'prostate' not in ''.join(report[1:5]).lower():
                    continue

                # if pair != ('26768028', '11/3/17'):
                #     continue

                if self.pairs and pair not in self.pairs:
                    continue

                data = self.extract_rep_data(empi, date, report)
                rad_dict[i] = list(pair) + data

        columns = ['MRN', 'Date', 'Accession Number', 'PIRADS', 'Prostate Volume', 'PSA', 'Race', 'Age']
        self.rad_df = pd.DataFrame.from_dict(rad_dict, orient='index', columns=columns).reset_index(drop=True)

        if self.debug:
            print(self.dem_df)
            print(self.clb_df)
            print(self.rad_df)
