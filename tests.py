"""
Program test script to be used for updates and bug fixes.
"""

import os
import glob
import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame

def extract_unique(frame, index, header):
    """
    Feed a data frame through this function along with the
    name and index of a column to extract all unique values.
    """
    col_frame = DataFrame(frame.iloc[:, [index]])
    unique_arr = col_frame[header].unique()

    return unique_arr

def file_name_check(name):
    """
    Feed a string through this function and it will check
    to see if the string contains any forbidden characters
    that cannot be used within file name. If it find one of
    these characters, the characters will be replaced by " - ".
    """
    exceptions = '\/:*?"<>|"'

    for char in name:
        if char in exceptions:
            name = name.replace(char, " - ")

    return name

def main():
    today = datetime.date.today()

    if not os.path.exists(f"./data/FP-UPC-{today}/Totals"):
        os.makedirs(f"./data/FP-UPC-{today}/Totals")

    if not os.path.exists("./excel/archive"):
        os.makedirs("./excel/archive")
        exit()

    file_name = "".join(glob.glob("./excel/*.xlsx"))
    xl_file = pd.read_excel(file_name)
    xl_file.rename(str.strip, axis="columns", inplace=True)

    upc_frame = DataFrame(xl_file[["UPC", "G/F", "PRODUCT GROUP"]])
    upc_frame.dropna(subset=["G/F", "PRODUCT GROUP"], inplace=True)

    gf_arr = extract_unique(upc_frame, 1, "G/F")
    prod_arr = extract_unique(upc_frame, 2, "PRODUCT GROUP")

    total_frame = DataFrame(upc_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)
    np.savetxt(r"./data/FP-UPC-{}/Totals/Totals - All.txt".format(today), total_frame.values, fmt="%s")

    for gf in gf_arr:
        gf_frame = upc_frame[upc_frame["G/F"] == gf]
        final_gf_frame = DataFrame(gf_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)

        np.savetxt(r"./data/FP-UPC-{}/Totals/Totals - {}.txt".format(today, gf), final_gf_frame.values, fmt="%s")

    for group in prod_arr:
        prod_frame = upc_frame[upc_frame["PRODUCT GROUP"] == group]
        final_prod_frame = DataFrame(prod_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)

        type_arr = extract_unique(prod_frame, 1, "G/F")
        type_label = "-".join(type_arr)
        group_label = file_name_check(group)

        np.savetxt(r"./data/FP-UPC-{}/{} - {}.txt".format(today, type_label, group_label), final_prod_frame.values, fmt="%s")

if __name__ == "__main__":
    main()
