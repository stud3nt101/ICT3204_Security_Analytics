import pandas as pd
import re


#### AUTH.LOG ####
def authlog(filename):
    # Create pandas dataframe
    df = pd.DataFrame([])

    # Open uploaded auth.log file
    with open(filename) as file:
        for line in file:
            '''
                Data obtained:
                1: Date & time stamp
                2: File path
                3: Process
                4: pam_unix
                5: Log information
            '''
            pattern = re.compile(
                "(.*?\s\d{2}\s\d{2}:\d{2}:\d{2})\s([A-Za-z]+)\s(\w*[\[\-\(\]]?\w+-?\w+[\]\[\=]?\w*[\]\)]?)"
                ":\s(pam_unix\(.*\):)?\s?(.*)")
            m = pattern.match(line)
            if m.group(4) is not None:
                pam = m.group(4)[:-1]
            else:
                pam = "NA"

            # Populate pandas dataframe
            df = df.append({
                'datetime': m.group(1),
                'filepath': m.group(2),
                'proc': m.group(3),
                'pam': pam,
                'info': m.group(5)
            }, ignore_index=True)

    # Write to dictionary
    data = df.to_dict("records")
    col = df.columns.values
    return data, col


#### History.log ####
def histlog(filename):
    # Create pandas dataframe
    df = pd.DataFrame([])

    # Open uploaded auth.log file
    with open(filename) as file:
        for line in file:
            '''
                Data obtained:
                1: Index
                2: Date & time stamp
                3: Bash command
            '''
            pattern = re.compile("\s+(\d+)\s+(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s(.*)")
            m = pattern.match(line)

            # Populate pandas dataframe
            df = df.append({
                'S/N': m.group(1),
                'datetime': m.group(2),
                'command': m.group(3)
            }, ignore_index=True)

    # Write to dictionary
    data = df.to_dict("records")
    col = df.columns.values
    print(data)
    return data, col

