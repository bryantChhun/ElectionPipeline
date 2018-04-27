#!/usr/bin/env python
# title           :file_considerations.py
# description     :see below
# author          :Bryant Chhun
# date            :10/25/2017
# version         :
# usage           : ./run.sh from root directory
# notes           :
# python_version  :3.6

# FileConsiderations uses class variables as flags when determining whether a line entry is valid
# you can set flags by passing a line into "set_flags"
# you can check flags by calling "check_flags",
#   which returns FALSE if line should be skipped
#   and returns a string for other specific actions

import datetime as dt


class FileConsiderations():

    def __init__(self):
        self.cmte_id_flag = True
        self.zip_flag = True
        self.transaction_dt_flag = True
        self.transaction_amt_flag = True
        self.other_id_flag = True
        self.invalid_line = False

    def set_flags(self, inputline):
        # inputline must be a single unnested list of 21 entries, conforming to FEC standards
        # True flags mean entry is valid or exists
        # False flags mean entry is invalid or does not exist

        #checking if line is complete
        if len(inputline) != 21:
            self.invalid_line = True
        else:
            self.invalid_line = False
        # checking for CMTE_ID validity
        if inputline[0]:
            self.cmte_id_flag = True
        else:
            self.cmte_id_flag = False
        # checking for ZIP code validity
        if not inputline[10] or len(inputline[10]) < 5 or len(inputline[10]) > 9:
            self.zip_flag = False
        else:
            self.zip_flag = True
        # checking for TRANSACTION_DT validity
        try:
            dt.datetime.strptime(inputline[13], "%m%d%Y")
            self.transaction_dt_flag = True
        except ValueError:
            self.transaction_dt_flag = False
        # checking for TRANSACTION_AMT validity
        if inputline[14]:
            self.transaction_amt_flag = True
        else:
            self.transaction_amt_flag = False
        # checking for OTHER_ID
        if inputline[15]:
            self.other_id_flag = True
        else:
            self.other_id_flag = False

        return None

    def check_flags(self):
        if self.invalid_line == True:
            return False
        if self.other_id_flag == True:
            return False
        if self.cmte_id_flag == False:
            return False
        if self.transaction_amt_flag == False:
            return False
        if self.transaction_dt_flag == False:
            # consider for medianvals_by_zip.txt
            # do NOT consider for medianvals_by_date.txt
            return "consider_for_zip"
        if self.zip_flag == False:
            # consider for medianvals_by_date.txt
            # do NOT consider for medianvals_by_zip.txt
            return "consider_for_date"
        else:
            return "consider_for_zipdate"