# simple pipeline to calculate a few values out of election data

PROJECT REQUIREMENTS:
- Python 3.6
- Python Libraries: CSV, time, numpy, functools, copy, os, sys (these should all be part of the Python 3.6 standard library)

CONSIDERATIONS:
- I use command line alias "python" to call python3.  Please make sure your terminal enviroment alias is set appropriately.
- run.sh should already be executable

PROGRAM STRUCTURE:
The program requires five files:
- execute.py
- file_considerations.py
- file_management.py
- medianvals.py
- run.sh file

- file_management.py contains the FileManagement class and "file_input" and "file_output" methods.  
- file_considerations.py contains the FileConsiderations class and the "set_flags" and "check_flags" methods.
    FileConsiderations class also initializes instance booleans: 
    cmte_id_flag, zip_flag, transaction_dt_flag, transaction_amt_flag, other_id_flag, invalid_line
- medianvals.py contains the MedianVals class and the "medianvals_by_date", "calculate_medianvals_by_date", 
    "medianvals_by_zip", and "nonbankers_rounding"
    MedianVals class also initializes instance structures:
    medianzip_out (list), medianzip_dict = (dictionary, medianzip_totals = (dictionary)
    mediandate_out = (list), mediandate_dict = (dictionary), mediandate_totals = (dictionary)
  
METHODOLOGY:
- I use class variables to store calculations and flags and then call them during file writing.  This means you can call those variable at any time, or pass them to a UI to get current-state values.
- Every line passes first through FileConsiderations, which sets the booleans for whether the line should be accepted and what action to take.
- medianvals accepts the results that pass through FileConsiderations and then extracts values based on ID, DATE or ZIP, and AMT of contribution.  All values are written to one of the above instance structures.

OPTIMIZATION:
- I store amounts in np.arrays for medianzip and mediandate dictionaries because the keys are hashable and ID/DATE and ID/ZIP lookup is O(1)
- I tested amt value as np.array, lists and tuples and found that np.array with np.median(overwrite_input=True) gave best performance and seemingly did not affect the output.

MY TESTS:
- I have tests under bryant_testsuite.py that you can run using run_bryants_tests.sh.  You'll have to comment out the lines under the .sh script to select those tests you want to run.
- Because the 1 million line file is too large for github, i've left that out.  It would need to be regenerated (also a command in the .sh script) in order for that particular test to run.
