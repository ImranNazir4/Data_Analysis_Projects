import os
import re

import pandas as pd
import tqdm

from parser.utils import get_header_indices, iter_reports


class BiopParser:
    def __init__(self, biop_fp=None, pairs=None, debug=False):
        # biop_fp: file path to the biopsy file
        # pairs: list of pairs containing the names of patients and the associated biopsy files
        # debug: whether to enable debugging output
        self.biop_fp = biop_fp
        self.pairs = pairs
        self.debug = debug

        # The pandas DataFrame that will store the biopsy data after parsing
        self.biop_df = None

    def are_files_ready(self):
        """
        Basic validation that filepaths are set and exist.
        """
        # Check if the file paths are not None and the files exist
        ready = [
            fp is not None and os.path.exists(fp)
            for fp in [self.biop_fp]
        ]

        return all(ready)  # True if all filepaths are valid
    def get_clinic_reports(self.biop_fp):
   
        report=report.split('\n')
        for i,j in enumerate(report):
            if j.strip()=='CLINICAL HISTORY':
                if 'prostate' in j.lower():
                    print(report[i+1])
        
        

    def get_diag_text(self, report):
        """
        Parses out final diagnosis section with spaces stripped from the tails of every line.
        """
        # Strip the spaces from the end of each line in the report
        rep = [line.strip(' ') for line in report]

        start = True
        terminal_phrases = ['Electronically signed', '**', 'GROSS DESCRIPTION']
        left = 0
        right = len(rep)
        for i, line in enumerate(rep):
            # Find the starting line of the final diagnosis section
            if start and ('FINAL DIAGNOSIS' in line or 'FINAL PATHOLOGIC DIAGNOSIS' in line):
                left = i
                start = False
            # Find the ending line of the final diagnosis section
            elif not start and (any([phrase in line for phrase in terminal_phrases])):
                right = i
                break
        return ''.join(rep[left:right])

    def parse_core_data(self, text):
        """
        Parses core length, core percent, and number of cores from a text.
        """
        core_length = core_percent = None
        # Parse the core length in mm
        search = re.search(r'(\d+\.?\d*)\s?mm', text)
        if search:
            core_length = float(search.group(1))

        # Parse the core percent
        search = re.search(r'(\d+)\s?%', text)
        if search:
            core_percent = int(search.group(1))

        p_cores = 0

        # Search for the number of cores involved
        searches = {
            0: r'cores involved.*?(\d)\sof\s\d',
            1: r'cores involved.*?(\d)\s?\/\s?\d'
        }
        for i in searches:
            search = re.search(searches[i], text)
            if search:
                p_cores = int(search.group(1))

        return core_length, core_percent, p_cores


    def parse_gleason(self, text):
        """Extracts gleason scores from diagnosis text.
        """
        g1 = None
        g2 = None
        gs = None

        # Set of regular expressions to search for gleason scores in text
        searches = {
            0: r'(\d+).*?(out\s)?of\s5\sand\s(\d+).*?(out\s)?of\s5',  # i.e. 3 of 5 and 4 of 5
            1: r'(\d)\s*?and\s*?(\d).*?(out\s)?of\s5',  # i.e. 3 and 4 of 5
            2: r'(\d)\s*?\+\s*?(\d)',  # i.e. 3+3 or 3 + 3
            3: r'(\d0?)\s*?(out\s)?of\s5',  # i.e. 3 of 5 or 3 out of 5
            4: r'(\d0?)\s*?(out\s)?of\s10',  # i.e. 6 of 10 or 6 out of 10
            5: r'(\d0?)\/5',  # i.e. 3/5
            6: r'(\d0?)\/10',  # i.e. 6/10
            7: r'score.*?of\s(\d0?)',  # i.e. score of 6
            8: r'score\s(\d)',  # i.e. score 6
            9: r'grade\s(\d)'  # i.e. grade 3
        }

        for i in range(len(searches)):
            search = re.search(searches[i], text)

            if search is None:
                continue

            if i == 0:
                g1 = int(search.group(1))
                g2 = int(search.group(3))
            elif i == 1 or i == 2:
                g1 = int(search.group(1))
                g2 = int(search.group(2))
            elif i == 3 or i == 5 or i == 9:
                g1 = g2 = int(search.group(1))
            elif i == 4 or i == 6 or i == 7 or i == 8:
                g1 = int(search.group(1)) // 2
                g2 = int(search.group(1)) - g1
            
            gs = g1 + g2
            break

        return g1, g2, gs

    def extract_rep_data(self, report):
        """Extracts data from a pathology report.
        """
        diagnosis = self.get_diag_text(report) # get the diagnosis data

        # Initialize the data
        gleason1 = -1
        gleason2 = -1
        gleason_score = -1
        gleason_dict = []
        pin = False
        atypia = False
        core_length = -1
        core_percent = -1
        pos_cores = 0

        lines = [l.lower() for l in diagnosis.split('\n\n') if l != ''] # split the diagnosis into lines
        for i, line in enumerate(lines): # iterate through the lines
            if self.debug:
                print(line)

            if line.startswith('note'):  # skip diagnosis notes
                continue

            if 'gleason' in line or 'carcinoma' in line:
                if i < len(lines) - 1 and lines[i+1].startswith('note'):  # check for note
                    line += '\n' + lines[i+1]

                g1, g2, gs = self.parse_gleason(line) # parse the gleason score

                if gs is not None and gs >= gleason_score:
                    gleason1 = g1
                    gleason2 = g2
                    gleason_score = gs
                
                elif gs is not None and gs == gleason_score:
                    if g1 > gleason1:
                        gleason1 = g1
                        gleason2 = g2
                    
                core_len, core_per, p_cores = self.parse_core_data(line)

                # Get the longest core length and highest core percent
                if core_len is not None and core_per is not None and core_len > core_length and core_per > core_percent:
                    core_length = core_len
                    core_percent = core_per

                if p_cores == 0 and gs is not None:
                    pos_cores += 1
                else:
                    pos_cores += p_cores

            pin = pin or 'prostatic intraepithelial neoplasia' in line or 'prostatic intra epithelial neoplasia' in line or 'pin' in line
            atypia = atypia or 'atyp' in line

        # Set negative values to None
        if core_length < 0:
            core_length = None
        if core_percent < 0:
            core_percent = None

        # Set diagnosis
        if gleason_score > 0:
            diag = 'PCa'
        else:
            gleason1 = None
            gleason2 = None
            gleason_score = None

            if pin and atypia:
                diag = 'Atypia/PIN'
            elif pin:
                diag = 'PIN'
            elif atypia:
                diag = 'Atypia'
            else:
                diag = 'Benign'
            
        return [diag, gleason1, gleason2, gleason_score, pos_cores, core_length, core_percent]

    def build_dfs(self):
        """Builds the dataframes for the biopsy and pathology reports.
        """
        if not self.are_files_ready():
            raise RuntimeError("Biopsy filepaths invalid/not set")

        biop_dict = {}
        with open(self.biop_fp) as bf:
            #header_i = get_header_indices(bf.readline())
            #print(header_i)
            for line in bf: # Did this instead so only the correct line gets passed to the function (the line that has '|')
                if '|' in line:
                    header_i = get_header_indices(line)
                    break

            for i, report in enumerate(tqdm.tqdm(iter_reports(bf))):
                while report[0] == '\n':
                    report.pop(0)
                header = report[0].split('|')
                
                empi = str(header[header_i['EMPI']])
                mrn = str(header[header_i['MRN']])
                date = pd.to_datetime(header[header_i['Report_Date_Time']]).strftime("%m/%d/%y")
                pair = (mrn, date)

                if 'prostat' not in ' '.join(report).lower():
                    continue

                if '\n' not in header: # Only run in the correct loop
                    date_index = header_i.get('Report_Date_Time')
                    date_unformatted = header[int(date_index)]
                    date = pd.to_datetime(date_unformatted).strftime("%m/%d/%y")

                    mrn_type_index = header_i.get('MRN_Type')
                    mrn_type = header[int(mrn_type_index)]
                            
                    data_set = (empi, mrn, date, mrn_type)
                    # pair = (mrn, date)
                    
                    rep_text_index = header_i.get('Report_Text')
                    rep_text_unformatted = (header[int(rep_text_index)])
                    rep_text = re.findall(r"Accession Number:\s+[A-Z0-9-]+", rep_text_unformatted)[0]
                    rep_text = rep_text.split(" ")[-1]
                    
                    brigham = False
                    
                    if 'prostatectomy' in ' '.join(report).lower(): # Skip prostatectomy reports
                        continue
                    
                    if 'prostat' not in ' '.join(report).lower():
                        continue
                    
                    if 'brigham' in ' '.join(report).lower(): 
                        brigham = True
                    

                    if self.pairs and data_set not in self.pairs:
                        continue

                    data = self.extract_rep_data(report)
                    # add brigham
                    biop_dict[i] = list(data_set) + data + [brigham] + [rep_text]

        # columns = ['MRN', 'Date', 'Diagnosis', 'Gleason1', 'Gleason2', 'GS', 'Pos Cores', 'Core Length', 'Core Percent']
        columns = ['EMPI', 'MRN', 'Date', 'MRN_Type', 'Diagnosis', 'Gleason1', 'Gleason2', 'GS', 'Pos Cores', 'Core Length', 'Core Percent', 'Brigham', 'Accession']
        self.biop_df = pd.DataFrame.from_dict(biop_dict, orient='index', columns=columns).reset_index(drop=True)
        total_mrn, total_mrn_unique = self.biop_df['MRN'].count(), self.biop_df['MRN'].nunique()
        # print(f"\nTotal MRNs: {total_mrn}, Unique MRNs: {total_mrn_unique}")

        if self.debug:
            print(self.biop_df)
