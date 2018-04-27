#!/usr/bin/env python
# title           :medianvals.py
# description     :see below
# author          :Bryant Chhun
# date            :10/26/2017
# version         :
# usage           : ./run.sh from root directory
# notes           :
# python_version  :3.6

# think about how to use only one class method, medianvals, to create dictionaries.  The user will instantiate two GeneralMedianVals classes,
#   one for ZIP and another for DATE.  Each class will possess its own dictionary
#   how does one manage the outputs?  for ZIP it is a running median for DATE it is calculated once
#       - we can have a method for calculating median_DATE as before
#       - we need a method that appends median_out specifically for the case with running_median_ZIP

import numpy as np
from functools import lru_cache as cache


class GeneralMedianVals():

    def __init__(self):
        #the following dictionaries and lists should always be of the same format:
        # [ID,ZIP,MEDIAN,NUMBER_of_CONTRIBUTIONS,TOTAL_CONTRIBUTIONS]

        self.median_dict = {}
        self.median_totals = {}
        self.median_out = []

    def medianvals(self, pipelinedata, cat1, cat2):
        #cat1 and cat2 are specific entries from pipeline data
        # cat1 and cat2 should be either ID DATE or ID ZIP
        amt = pipelinedata[14]
        if not self.median_dict or (cat1, cat2) not in self.median_dict:
            self.median_dict[cat1, cat2] = np.array([int(amt)])
            self.median_totals[cat1, cat2] = int(amt)
        elif (cat1, cat2) in self.median_dict:
            self.median_dict[cat1, cat2] = np.append(self.median_dict[cat1, cat2], int(amt))
            self.median_totals[cat1, cat2] += int(amt)
        return None

    def update_median_out(self, cat1, cat2):
        self.median_out.append([cat1,
                                cat2,
                                str(self.nonbankers_rounding(np.median(self.median_dict[cat1, cat2], overwrite_input=True))),
                                str(len(self.median_dict[cat1,cat2])),
                                str(self.median_totals[cat1,cat2])
                                ])
        return None

    def calculate_medianvals(self):
        for cat1, cat2 in self.median_dict:
            self.median_out.append([cat1,
                                    cat2,
                                    str(self.nonbankers_rounding(np.median(self.median_dict[cat1, cat2], overwrite_input=True))),
                                    str(len(self.median_dict[cat1, cat2])),
                                    str(self.median_totals[cat1, cat2])
                                    ])
        self.median_out = sorted(self.median_out, key=lambda x: (x[0], x[1]))
        return None


    # Use a cache here because there are limits to $ amt of campaign contributions
    # and thus a limited space of medians that can be calculated.
    @cache(maxsize=None)
    def nonbankers_rounding(self, floatval):
        i, j = divmod(floatval, 1)
        return int(i + ( (j >= 0.5) if (floatval > 0) else (j > 0.5)))