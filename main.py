# Author: Ayelet Zadock
# Last modified: Jul 02 2023

# Imports:
from CSVfile import *

def main():
    filename = FILENAME
    csv_file = CSVfile(filename)  # create an implementation of CSVfile
    print(f'Amount of lines in file: {csv_file.get_len()}')
    print(f'Type of good index: {csv_file.get_type_by_index(1)}')
    print(f'Type of bad index: {csv_file.get_type_by_index(4000)}')
    print(f'Length of good index: {csv_file.calculate_length_by_index(1)}')
    print(f'Length of bad index: {csv_file.calculate_length_by_index(4000)}')
    print(f'Area of good index: {csv_file.calculate_area_by_index(1)}')
    print(f'Area of bad index: {csv_file.calculate_area_by_index(4000)}')
    print(f'Maximum length of good type: {csv_file.get_max_length(1)}')
    print(f'Maximum length of bad type: {csv_file.get_max_length(0)}')
    print(f'Maximum area of good type: {csv_file.get_max_area(2)}')
    print(f'Maximum area of bad type: {csv_file.get_max_area(0)}')
    csv_file.close_session()  # release file from memory


if __name__ == "__main__":
    main()
