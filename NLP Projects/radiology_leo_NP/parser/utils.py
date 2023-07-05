# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 17:40:04 2023

@author: n
"""


# Header Names:
#     ['EMPI', 'EPIC_PMRN', 'MRN_Type', 'MRN', 'Report_Number', 'Report_Date_Time', 'Report_Description', 'Report_Status', 'Report_Type', 'Report_Text']

def get_header_indices(header):
    """
    This function takes the header of the input file as a string and returns a dictionary mapping
    each header name to its index in the header.
    
    Inputs:
        header: a string representing the header of the input file, separated by '|'
    
    Outputs:
        A dictionary mapping each header name to its index in the header.
    """
    headers = header.strip().split('|')
    return {header: i for i, header in enumerate(headers)}


def get_mrn_date_pairs(df):
    """
    This function takes a DataFrame as input and returns a set of tuples, each tuple containing a 
    MRN and date from the input DataFrame.
    
    Inputs:
        df: a pandas DataFrame
    
    Outputs:
        A set of tuples, each tuple containing a MRN and date from the input DataFrame.
    """
    df = df[['MRI fu 2::unit', 'MRI fu 2::Date']]

    pairs = set()
    for _, row in df.iterrows():
        pairs.add((row['MRI fu 2::unit'], row['MRI fu 2::Date']))

    return pairs


def iter_reports(file):
    """
    This function takes an open file object as input and yields lists of strings, each list representing
    a report in the file.
    
    Inputs:
        file: an open file object
    
    Yields:
        Lists of strings, each list representing a report in the file.
    """
    report = []

    for line in file:
        if line.strip() != '[report_end]':
            report.append(line)
        else:
            while report[0] == '\n':
                report = report[1:]
            yield report
            report = []


def common_date_formats(date):
    """
    This function takes a date as input and returns a list of common date formats that can be 
    used to represent the date as a string.
    
    Inputs:
        date: a date
    
    Outputs:
        A list of common date formats that can be used to represent the date as a string.
    """
    return [
        date.strftime("%m/%d/%Y"),
        date.strftime("%-m/%-d/%Y"),
        date.strftime("%m/%d/%y"),
        date.strftime("%-m/%-d/%y")
    ]
