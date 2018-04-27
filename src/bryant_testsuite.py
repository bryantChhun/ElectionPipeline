#!/usr/bin/env python
# title           :bryant_testsuite.py
# description     :
# author          :Bryant Chhun
# date            :10/26/2017
# version         :
# usage           : comment out lines as needed from ./run_bryants_tests.sh, then run from root directory
# notes           :
# python_version  :3.6

# This test suite can create several data sets:
# - 1 million line entries in a file, randomly selected from the "template" entries in itcont.txt
# - 500k line entries as above
# - 100k line entries as above
# - "easy_median" which outputs 100k lines of a single qualified donor.  Each contribution is amt=1
# - "random_amts" which outputs 100k lines of a random donors.  Each contribution is randomly modified +/- $500
# - "invalid_entries" which outputs 100k lines of unqualified entries EXCEPT one: CMTE_ID = "TRUE_ZIP"


import numpy as np
import sys
import csv
from copy import deepcopy
from file_considerations import FileConsiderations


class TestSuite():

    def __init__(self):
        self.input_file = None
        self.file_path = None
        self.num_entries = 0
        self.file_name = None

    def get_template_data(self, template_file):
        report = []
        with open(template_file, 'r') as txtin:
            data = txtin
            for line in data:
                report.append(line.strip().split("|"))
        return report

    def create_fixed_amts_mega_file(self, template_in, num_entries):
        fixed_amts_list = []
        selection = template_in[np.random.randint(0, len(template_in))]
        for k in range(num_entries):
            selection[14] = str(k)
            fixed_amts_list.append(deepcopy(selection))
        return fixed_amts_list

    def create_randomized_amts_mega_file(self, template_in, num_entries):
        random_mega_list = []
        for k in range(num_entries):
            selection = template_in[np.random.randint(0, len(template_in))]
            selection[14] = str(abs(int(selection[14]) + np.random.randint(-500, 500)))
            random_mega_list.append(deepcopy(selection))
        return random_mega_list

    def create_mega_file(self, template_in, num_entries):
        mega_list = []
        for k in range(num_entries):
            mega_list.append(template_in[np.random.randint(0, len(template_in))])
        return mega_list

    def create_custom_data(self, template_line, cmte_id, zip, trans_dt, trans_amt, other_id):
        if len(template_line) != 21:
            print("must be single line")
            return None
        newline = deepcopy(template_line)
        newline[0] = str(cmte_id)
        newline[10] = str(zip)
        newline[13] = str(trans_dt)
        newline[14] = str(trans_amt)
        newline[15] = str(other_id)
        return newline

    def create_false_file(self, template_in, num_entries):
        false_list = []
        FileConsider = FileConsiderations()
        line = template_in[np.random.randint(0, len(template_in))]
        FileConsider.set_flags(line)
        while FileConsider.check_flags() != False:
            falseother = self.create_custom_data(line, "FALSE_OTHER_ID", "60069", '01012017', '100', 'falseID')
            falsedate1 = self.create_custom_data(line, "FALSE_DATE1", "60069", '31012017', '100', '')
            falsedate2 = self.create_custom_data(line, "FALSE_DATE2", "60069", '0101201', '100', '')
            falsezip1 = self.create_custom_data(line, "FALSE_ZIP1", "", '01012017', '100', '')
            falsezip2 = self.create_custom_data(line, "FALSE_ZIP2", "6006", '01012017', '100', '')
            falsezip3 = self.create_custom_data(line, "FALSE_ZIP3", "6006900001", '01012017', '100', '')
            truezip1 = self.create_custom_data(line, "TRUE_ZIP", "60069", '01012017', '100', '')
            falsecmteid = self.create_custom_data(line, '', "60069", '01012017', '100', '')
            falseamt = self.create_custom_data(line, "FALSE_AMT", "60069", '01012017', '', '')
            line = template_in[np.random.randint(0, len(template_in))]
            FileConsider.set_flags(line)
        false_lines = [falseother, falsedate1, falsedate2, falsezip1, falsezip2, falsezip3, truezip1, falsecmteid, falseamt]
        for k in range(num_entries):
            false_list.append(false_lines[np.random.randint(0, len(false_lines))])
        return false_list

    def file_output_csv(self, file_path, file_name, data):
        # data should be nested list, which will be output
        with open(file_path + "/" + file_name, 'w', newline='') as writefile:
            w = csv.writer(writefile, delimiter='|')
            for entry in data:
                w.writerow(entry)
        return None

    def test_output(self, file_path, file_name):
        with open(file_path + "/" + file_name, 'r', newline='') as testfile:
            for line in testfile:
                print(line)
        return None

def main():
    tester = TestSuite()

    tester.input_file = sys.argv[1]
    tester.output_path = sys.argv[2]
    tester.file_name = sys.argv[3]
    tester.num_entries = 100000

    template = tester.get_template_data(tester.input_file)

    if sys.argv[3] == '100k_easy_median.txt':
        mega = tester.create_fixed_amts_mega_file(template, tester.num_entries)
    if sys.argv[3] == '100k_invalid_entries.txt':
        mega = tester.create_false_file(template, tester.num_entries)
    if sys.argv[3] == '100k_random_amts.txt':
        mega = tester.create_randomized_amts_mega_file(template, tester.num_entries)
    if sys.argv[3] == '100k_entries.txt':
        tester.num_entries = 100000
        mega = tester.create_mega_file(template, tester.num_entries)
    if sys.argv[3] == '500k_entries.txt':
        tester.num_entries = 500000
        mega = tester.create_mega_file(template, tester.num_entries)
    if sys.argv[3] == '1m_entries.txt':
        tester.num_entries = 1000000
        mega = tester.create_mega_file(template, tester.num_entries)



    tester.file_output_csv(tester.output_path, tester.file_name, mega)

if __name__ == '__main__':
    main()
