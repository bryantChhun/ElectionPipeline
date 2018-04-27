#!/usr/bin/env python
# title           :medianvals.py
# description     :see below
# author          :Bryant Chhun
# date            :10/26/2017
# version         :
# usage           : ./run.sh from root directory
# notes           :
# python_version  :3.6


# MedianVals class contains three class variables that store our values of interest:
# @ represents either ZIP or DATE
# median@_out = nested list that is used by file_management to write the data to file
# median@_dict = dictionary whose keys are a pair of ID and ZIP/DATE and whose value is a list of contribution amounts
# median@_totals = dictionary whose keys are a pair of ID and ZIP/DATE and whose value is a running sum of contribution amounts
#
# functions "medianvals_by_date" and "medianvals_by_zip" are nearly identical except that
#   "_by_date" medians are calculated all at once using "calculate_medianvals_by_date"
#
# if we would send data to a GUI, then functions "medianvals_by_date" and "medianvals_by_zip" would
#   return the last value of median@_out
#

import numpy as np
from functools import lru_cache as cache


class MedianVals():

    def __init__(self):
        #the following dictionaries and lists should always be of the same format:
        # [ID,ZIP,MEDIAN,NUMBER_of_CONTRIBUTIONS,TOTAL_CONTRIBUTIONS]

        self.medianzip_out = []
        self.medianzip_dict = {}
        self.medianzip_totals = {}

        # [ID,DATE,MEDIAN,NUMBER_of_CONTRIBUTIONS,TOTAL_CONTRIBUTIONS]
        self.mediandate_out = []
        self.mediandate_dict = {}
        self.mediandate_totals = {}

    def medianvals_by_date(self, pipelinedata):
        # pipelinedata: normal 21 column
        # outputformat, str: ID|DATE|MEDIAN|NUMBER_of_CONT_by_ID-DATE|TOTAL
        ID = pipelinedata[0]
        DATE = pipelinedata[13]
        amt = pipelinedata[14]
        if not self.mediandate_dict or (ID, DATE) not in self.mediandate_dict:
            self.mediandate_dict[ID, DATE] = np.array([int(amt)])
            self.mediandate_totals[ID, DATE] = int(amt)
        elif (ID, DATE) in self.mediandate_dict:
            self.mediandate_dict[ID, DATE] = np.append(self.mediandate_dict[ID, DATE], int(amt))
            self.mediandate_totals[ID, DATE] += int(amt)
        return None

    def calculate_medianvals_by_date(self):
        for ID, DATE in self.mediandate_dict:
            self.mediandate_out.append([ID,
                                        DATE,
                                        str(self.nonbankers_rounding(np.median(self.mediandate_dict[ID, DATE], overwrite_input=True))),
                                        str(len(self.mediandate_dict[ID,DATE])),
                                        str(self.mediandate_totals[ID,DATE])
                                        ])
        self.mediandate_out = sorted(self.mediandate_out, key=lambda x: (x[0], x[1]))
        return None

    def medianvals_by_zip(self, pipelinedata):
        # pipelinedata: normal 21 column
        # outputformat/recent_entry, str: ID|ZIP|MEDIAN|NUMBER_of_CONT_byID-ZIP|TOTAL
        # It's faster to use np.array as medianzip_dict value, then calculate np.median with overwrite_input=True, than with using tuples
        # However, tuples are slightly faster than lists when using np.median.
        ID = pipelinedata[0]
        ZIP = pipelinedata[10][0:5]
        amt = pipelinedata[14]
        if not self.medianzip_dict or (ID, ZIP) not in self.medianzip_dict:
            #self.medianzip_dict[ID, ZIP] = (float(amt),)
            self.medianzip_dict[ID, ZIP] = np.array([int(amt)])
            self.medianzip_totals[ID, ZIP] = int(amt)
            self.medianzip_out.append([ID, ZIP, amt, 1, amt])
            return None
        elif (ID, ZIP) in self.medianzip_dict:
            #self.medianzip_dict[ID, ZIP] += (float(amt),)
            self.medianzip_dict[ID, ZIP] = np.append(self.medianzip_dict[ID, ZIP], int(amt))
            self.medianzip_totals[ID, ZIP] += int(amt)
            self.medianzip_out.append([ID,
                                       ZIP,
                                       str(self.nonbankers_rounding(np.median(self.medianzip_dict[ID, ZIP], overwrite_input=True))),
                                       str(len(self.medianzip_dict[ID, ZIP])),
                                       str(self.medianzip_totals[ID, ZIP])
                                       ])
            return None

    # Use a cache here because there are limits to $ amt of campaign contributions
    # and thus a limited space of medians that can be calculated.
    @cache(maxsize=None)
    def nonbankers_rounding(self, floatval):
        i, j = divmod(floatval, 1)
        return int(i + ( (j >= 0.5) if (floatval > 0) else (j > 0.5)))