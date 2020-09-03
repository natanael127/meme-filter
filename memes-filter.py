#!/usr/bin/env python

#TODO: constants to parameters, readme, keyboard interrupt
# ============================================================ IMPORTS
import pytesseract
import os
import shutil
import time #Just tests

# ============================================================ CONSTANTS
DIR_TEXTUAL = "./Textual"
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

# ============================================================ MAIN SCRIPT
files = list_all_files_recursevely(".", DIR_TEXTUAL)
total = len(files)
counter_positive = 0
for k in range(total):
    curr_str = ""
    try:    
        curr_str = pytesseract.image_to_string(files[k])
    except:
        pass
    if (count_valid_chars(curr_str) > CHAR_THRESHOLD):
        counter_positive += 1
        print (str(counter_positive).zfill(4) + " - " + str(k).zfill(4) + " - " + str(total).zfill(4))
        shutil.move(files[k], DIR_TEXTUAL)

