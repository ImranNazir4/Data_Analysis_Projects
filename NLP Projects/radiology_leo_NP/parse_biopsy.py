# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 16:47:44 2023

@author:
"""

import argparse
import os
## import parser ##
import pandas as pd

# Import the custom BiopParser class
from parser.BiopParser import BiopParser


def main(biop_filepath, ann_filepath=None, debug=False, clean=False):
    # Set the file path for the output CSV file
    biop_output_filepath = './data/biop_output.csv'

    # Initialize the annotation dataframe as None
    ann_df = None
    
    # If an annotation file is provided
    if ann_filepath:
        ann_df = pd.read_csv(ann_filepath, sep='\t', dtype={'biopsies::unit': str})
        ann_df.rename(columns={'biopsies::unit': 'MRN', 'biopsies::date': 'Date'}, inplace=True)
        
        # Convert the date column to a string representation in the format "%-m/%-d/%y"
        ann_df['Date'] = pd.to_datetime(ann_df['Date']).dt.strftime("%m/%d/%y")

        # If in debug mode, print the number of annotations
        if debug:
            print("num annotations: ", len(ann_df))

    # If the "clean" flag is not set and a biop_output file already exists
    if not clean and os.path.exists(biop_output_filepath):
        # Read the existing biop_output file into a pandas dataframe
        biop_df = pd.read_csv(biop_output_filepath, dtype={'MRN': str})
    else:
        # Initialize the pairs set as None
        pairs = None
        
        # If the annotations dataframe is not None
        if ann_df is not None:
            pairs = set()

            # For each row in the annotations dataframe
            for _, row in ann_df.iterrows():
                # Add the MRN and date as a tuple to the pairs set
                pairs.add((row['EMPI'], row['MRN'], row['Date']))

        # Initialize an instance of the BiopParser class with the biop file path and pairs set
        biop_parser = BiopParser(biop_fp=biop_filepath, pairs=pairs, debug=debug)
        
        # Build the biop dataframes
        biop_parser.build_dfs()

        # Sort the biop dataframe by the Gleason Score column
        biop_df = biop_parser.biop_df.sort_values(by=['GS'], na_position='last')
        
        # Drop duplicate rows in the biop dataframe based on the EMPI, MRN and date columns, keeping only the first instance
        # biop_df = biop_df.drop_duplicates(subset=['EMPI', 'MRN', 'Date'], keep='first').sort_index().reset_index(drop=True)
        biop_df = biop_df.drop_duplicates(subset=['MRN', 'Date'], keep='first').sort_index().reset_index(drop=True)

        # Save the biop dataframe to a CSV file
        biop_df.to_csv(biop_output_filepath, index=False) 
        print(biop_df)

    if ann_df is not None:
        columns = [
            'EMPI', 'MRN', 'Date', 'biopsies::finding', 'Diagnosis',
            'biopsies::Gleason1', 'Gleason1', 'biopsies::Gleason2', 'Gleason2', 'biopsies::GS', 'GS',
            'biopsies::pos_cores', 'Pos Cores', 'biopsies::Corelength', 'Core Length', 'biopsies::Corepercent',             'Core Percent'
        ]
        df = ann_df.merge(biop_df, how='inner', on=['MRN', 'Date'])[columns]

        print('Diagnosis: {:.3f}'.format(sum(df['biopsies::finding'] == df['Diagnosis']) / len(df)))

        temp_df = df.dropna(subset=['biopsies::GS', 'GS'], how='all') # drop only if both are none. 
        print('Gleason1: {:.3f}'.format(sum(temp_df['biopsies::Gleason1'] == temp_df['Gleason1']) / len(temp_df)))
        print('Gleason2: {:.3f}'.format(sum(temp_df['biopsies::Gleason2'] == temp_df['Gleason2']) / len(temp_df)))
        print('Gleason Score: {:.3f}'.format(sum(temp_df['biopsies::GS'] == temp_df['GS']) / len(temp_df)))

        temp_df = df.dropna(subset=['biopsies::pos_cores', 'Pos Cores'], how='all')
        print('Positive Cores: {:.3f}'.format(sum(temp_df['biopsies::pos_cores'] == temp_df['Pos Cores']) / len(temp_df)))
        temp_df = df.dropna(subset=['biopsies::Corelength', 'Core Length'], how='all')
        print('Core Length: {:.3f}'.format(sum(temp_df['biopsies::Corelength'] == temp_df['Core Length']) / len(temp_df)))
        temp_df = df.dropna(subset=['biopsies::Corepercent', 'Core Percent'], how='all')
        print('Core Percent: {:.3f}'.format(sum(temp_df['biopsies::Corepercent'] == temp_df['Core Percent']) / len(temp_df)))

        temp_df = df.dropna(subset=['biopsies::GS', 'GS'], how='all')
        df = temp_df[temp_df['biopsies::GS'] != temp_df['GS']][['MRN', 'Date', 'biopsies::GS', 'GS']]

        df.to_csv('./data/diff.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--biop-file', type=str, default=r'C:\Users\drsmi\PycharmProjects\SybilX\scripts\mgh_prostate\radiology\rysn_Delivery\SybilX-neel-mgh-script\SybilX-neel-mgh-script\scripts\mgh_prostate\radiology\data\KS185_20230502_114833_Pat.txt',
        help="path to biopsy reports"
    )
    parser.add_argument(
        '--ann-file', type=str,
        help="path to biopsy annotations; will evaluate output with annotations"
    )
    parser.add_argument(
        '--debug', action='store_true',
        help="print debug messages"
    )
    parser.add_argument(
        '--clean', action='store_true',
        help="start from scratch"
    )

    args = parser.parse_args()

    main(args.biop_file, ann_filepath=args.ann_file, debug=args.debug, clean=args.clean)