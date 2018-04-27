#!/usr/bin/env python
# title           :execute.py
# description     :see below
# author          :Bryant Chhun
# date            :10/26/2017
# version         :
# usage           : ./run.sh from root directory
# notes           :
# python_version  :3.6

# main function


from file_management import FileManagement
from file_considerations import FileConsiderations
from medianvals import MedianVals
from generalized_medianvals import GeneralMedianVals
import time
import sys


def main():
    FileManager = FileManagement()
    FileConsider = FileConsiderations()
    Metrics = MedianVals()

    input_file = sys.argv[1]
    output_path = sys.argv[2]

    #report = FileManager.file_input(input_file)
    report = (line.strip().split("|") for line in open(input_file, 'r'))
    for line in report:
        FileConsider.set_flags(line)
        if FileConsider.check_flags() == False:
            continue
        elif FileConsider.check_flags() == "consider_for_zip":
            Metrics.medianvals_by_zip(line)
            continue
        elif FileConsider.check_flags() == "consider_for_date":
            Metrics.medianvals_by_date(line)
            continue
        elif FileConsider.check_flags() == "consider_for_zipdate":
            Metrics.medianvals_by_zip(line)
            Metrics.medianvals_by_date(line)
            continue

    # for line in report:
    #     FileConsider.set_flags(line)
    #     if FileConsider.check_flags() == False:
    #         continue
    #     elif FileConsider.check_flags() == "consider_for_zip":
    #         Metrics.medianvals_by_zip(line)
    #         continue
    #     elif FileConsider.check_flags() == "consider_for_date":
    #         Metrics.medianvals_by_date(line)
    #         continue
    #     elif FileConsider.check_flags() == "consider_for_zipdate":
    #         Metrics.medianvals_by_zip(line)
    #         Metrics.medianvals_by_date(line)
    #         continue

    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_zip.txt", data=Metrics.medianzip_out)

    Metrics.calculate_medianvals_by_date()
    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_date.txt", data=Metrics.mediandate_out)

def generalized_main():
    FileManager = FileManagement()
    FileConsider = FileConsiderations()
    ZIPMetrics = GeneralMedianVals()
    DATEMetrics = GeneralMedianVals()

    input_file = sys.argv[1]
    output_path = sys.argv[2]

    report = FileManager.file_input(input_file)
    for line in report:
        FileConsider.set_flags(line)
        if FileConsider.check_flags() == False:
            continue
        elif FileConsider.check_flags() == "consider_for_zip":
            ZIPMetrics.medianvals(line, line[0], line[10][0:5])
            ZIPMetrics.update_median_out(line[0], line[10][0:5])
            continue
        elif FileConsider.check_flags() == "consider_for_date":
            DATEMetrics.medianvals(line, line[0], line[13])
            continue
        elif FileConsider.check_flags() == "consider_for_zipdate":
            ZIPMetrics.medianvals(line, line[0], line[10][0:5])
            ZIPMetrics.update_median_out(line[0], line[10][0:5])
            DATEMetrics.medianvals(line, line[0], line[13])
            continue

    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_zip.txt", data=ZIPMetrics.median_out)

    DATEMetrics.calculate_medianvals()
    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_date.txt", data=DATEMetrics.median_out)


if __name__ == '__main__':
    start_time = time.time()
    main()
    #generalized_main()
    print("total time = ----------- %s seconds ------------" %(time.time() - start_time))