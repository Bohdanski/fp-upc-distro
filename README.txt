# FP UPC Distro

FP UPC Distro (Front Page UPC Distribution) is a script that takes in an Excel Workbook containing a list of product UPC's and their corresponding product groups. It then outputs a text file for each Product Group, and that groups associated UPC's. The files are named after the Product Group as well as a label if the group is Fresh or CS. Lastly the file will be placed into an archive folder for future reference.



# Installation

This program is mostly self contained within its folder. Where-ever you decide to place the folder, the path must be manually adjusted within the launcher.bat script.



# Usage

step 1 - Place the Excel file you wish to distribute within the "excel" folder.
step 2 - Double click on "launcher.bat" to run the script.
step 3 - Resulting text files may be retreived from the "data" folder under today's date.



# Versions

v1.0 - 01/23/2020 - Initial stable release
v1.1 - 01/24/2020 - Added functionality for outputting total lists for UPC's by all, and by GF type.
		  - Imporved code efficiency and readability.
v1.2 - 01/30/2020 - Fixed bug that used forbidden characters found in product groups within the file name.
		  - Improved code styling based on PEP-8 conventions.

# Author

Bohdan Tkachenko

