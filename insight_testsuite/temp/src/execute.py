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
import time
import sys


def main():
    FileManager = FileManagement()
    FileConsider = FileConsiderations()
    Metrics = MedianVals()

    input_file = sys.argv[1]
    output_path = sys.argv[2]

    #input_file = input_path
    #input_file = input_path + "itcont.txt"

    report = FileManager.file_input(input_file)
    #count = 0
    #loop_time = time.time()
    for line in report:
        #if count % 1000 == 0:
        #    print(str(count)+"th line, time per 1000 lines = ---- %s seconds ----" %(time.time() - loop_time))
        #    loop_time = time.time()
        #count += 1
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

    #print('writing zips')
    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_zip.txt", data=Metrics.medianzip_out)

    #print('calculating dates')
    #calculate_time = time.time()
    Metrics.calculate_medianvals_by_date()
    #print("time to calculate medianvals_by_date = ----------- %s seconds ------------" % (time.time() - calculate_time))
    #print('writing dates')
    FileManager.file_output(outputpath=output_path, outputname="medianvals_by_date.txt", data=Metrics.mediandate_out)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("total time = ----------- %s seconds ------------" %(time.time() - start_time))