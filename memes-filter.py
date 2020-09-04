#!/usr/bin/env python

#TODO: constants to parameters, readme, keyboard interrupt
# ============================================================ IMPORTS
import pytesseract
import os
import shutil
import numpy

# ============================================================ CONSTANTS
DIR_TEXTUAL = "./Textual"
DIR_MAIN = "."
CHAR_THRESHOLD = 40

# ============================================================ FUNCTIONS
def list_all_files_recursevely(father_directory, exception):
    files_list = []
    for root, dirs, files in os.walk(father_directory):
        if root != DIR_TEXTUAL:
            for filename in files:
                files_list.append(root + "/" + filename)
    return files_list

def count_valid_chars(the_string):
    result = 0
    string_list = map(ord, the_string)
    for ascii_num in string_list:
        if ascii_num >= 33 and ascii_num <= 126: #!~
            result += 1
    return result

def clear_screen():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

# ============================================================ MAIN SCRIPT
files = list_all_files_recursevely(DIR_MAIN, DIR_TEXTUAL)
files.sort()
total = len(files)
num_digits = int(numpy.floor(numpy.log(total) / numpy.log(10))) + 1
counter_positive = 0
for k in range(total):
    # Reads optically the file
    curr_str = ""
    try:    
        curr_str = pytesseract.image_to_string(files[k])
    except:
        pass
    # Checks if is a lot of text
    if (count_valid_chars(curr_str) > CHAR_THRESHOLD):
        counter_positive += 1
        # Handles repeated file names
        file_name = files[k].split("/")[-1] #With extension
        file_extension = file_name.split(".")[-1]
        file_name = file_name[0:len(file_name) - len(file_extension) - 1] #Without extension
        number_append = 0
        string_append = ""
        while os.path.isfile(DIR_TEXTUAL + "/" + file_name + "-" + string_append + "." + file_extension):
            number_append += 1
            string_append = str(number_append)
        # Moves the file
        shutil.move(files[k], DIR_TEXTUAL + "/" + file_name + "-" + string_append + "." + file_extension)
    # Print stats
    clear_screen()
    print("Analysed......: " + str(k + 1).rjust(num_digits))
    print("Positive cases: " + str(counter_positive).rjust(num_digits))
    print("Total.........: " + str(total).rjust(num_digits))

