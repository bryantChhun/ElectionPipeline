#!/usr/bin/env python
# title           :file_management.py
# description     :see below
# author          :Bryant Chhun
# date            :10/25/2017
# version         :
# usage           : ./run.sh from root directory
# notes           :
# python_version  :3.6

# FileManagement is a straightforward class that contains input/output functions
# one unused function, file_input_generator, was written to simulate "streaming" data from another source.

import csv


class FileManagement():

    def __init__(self):
        return None

    def file_input(self, file_path):
        report = []
        with open(file_path, 'r') as txtin:
            data = txtin
            for line in data:
                report.append(line.strip().split("|"))
        return report

    def file_input_generator(self, file_path):
        with open(file_path, 'r') as txtin:
            data = txtin
            for line in data:
                yield line.strip().split("|")

    def file_input_generator_2(self, file_path):
        yield (line.strip().split("|") for line in open(file_path, 'r'))

    # using newline='' with a csv writer helps with '/r/n' formatting.
    def file_output(self, outputpath, outputname, data):
        #data should be nested list, which will be output
        with open(outputpath +"/" + outputname, 'w', newline='') as writefile:
            w = csv.writer(writefile, delimiter='|')
            for entry in data:
                w.writerow(entry)
        return None

