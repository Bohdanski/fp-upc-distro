"""
Main working script, with block and inline comments to explain the code.
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
    """
    Main logic to be executed.
    """
    # Create a timestamp using todays date in DB format.
    today = datetime.date.today()

    # Check to see if the "Totals", today's data folder,
    # and the master data folder exist.
    # If they do not, create them.
    if not os.path.exists(f"./data/FP-UPC-{today}/Totals"):
        os.makedirs(f"./data/FP-UPC-{today}/Totals")

    # Check if the excel sub-directory exists.
    # If it does not create it, and then exit the program.
    if not os.path.exists("./excel/archive"):
        os.makedirs("./excel/archive")
        exit()

    # Look for any file with an .xlsx format within the "excel" folder,
    # open it as a Pandas DataFrame, then strip all leading and trailing
    # white spaces from the column headers.
    file_name = "".join(glob.glob("./excel/*.xlsx"))
    xl_file = pd.read_excel(file_name)
    xl_file.rename(str.strip, axis="columns", inplace=True)

    # Extract the desired columns into a new DataFrame.
    # If any rows in this new DataFrame have null values
    # for both "G/F" or "PRODUCT GROUP" delete them.
    upc_frame = DataFrame(xl_file[["UPC", "G/F", "PRODUCT GROUP"]])
    upc_frame.dropna(subset=["G/F", "PRODUCT GROUP"], inplace=True)

    # Using the new DataFrame that was made, feed it through
    # the extract function to get all unique values from
    # the Product Group and G/F columns.
    gf_arr = extract_unique(upc_frame, 1, "G/F")
    prod_arr = extract_unique(upc_frame, 2, "PRODUCT GROUP")

    # Save a total list of all UPC's
    total_frame = DataFrame(upc_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)
    np.savetxt(r"./data/FP-UPC-{}/Totals/Totals - All.txt".format(today), total_frame.values, fmt="%s")

    # Iterate through every unique G/F in gf_arr
    # and create a file for each one.
    for gf in gf_arr:
        # Using the master upc_frame, create a new DataFrame
        # for each G/F that is passed in. Then take the new
        # DataFrame and extract only the "UPC" column.
        # Incase of number format, remove any decimal values.
        gf_frame = upc_frame[upc_frame["G/F"] == gf]
        final_gf_frame = DataFrame(gf_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)

        # Save each new DataFrame that is extracted using the unique
        # G/F values by using the "gf" iterator as the file name.
        np.savetxt(r"./data/FP-UPC-{}/Totals/Totals - {}.txt".format(today, gf), final_gf_frame.values, fmt="%s")

    # Iterate through every unique Product Group
    # in prod_arr and create a file for each one.
    for group in prod_arr:
        # Using the master upc_frame, create a new DataFrame
        # for each Product Group that is passed in. Then take
        # the new DataFrame and extract only the "UPC" column.
        # Incase of number format, remove any decimal values.
        prod_frame = upc_frame[upc_frame["PRODUCT GROUP"] == group]
        final_prod_frame = DataFrame(prod_frame.iloc[:, [0]]).apply(lambda x: '%.0f' % x, axis=1)

        # Similar to how each unique product group is extracted,
        # the same is done for "G/F". However, only one value is expected.
        # This one value depending on the Product_Group type is then
        # assigned to a variable to be used within the output file name.
        # Lastly each product group is fed through the file_name_check function
        # to be checked for forbidden characters, and is saved to a variable.
        type_arr = extract_unique(prod_frame, 1, "G/F")
        type_label = "-".join(type_arr)
        group_label = file_name_check(group)

        # Save each new DataFrame that is extracted using the unique Product Group
        # names by using the "G/F" type, as well as the Product Group as the file name.
        np.savetxt(r"./data/FP-UPC-{}/{} - {}.txt".format(today, type_label, group_label), final_prod_frame.values, fmt="%s")

if __name__ == "__main__":
    main()
