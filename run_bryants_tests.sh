#!/bin/bash

#the bottom 5 commands create test data that are run by the next 5 lines
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_easy_median/input/ 100k_easy_median.txt
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_random_amts/input/ 100k_random_amts.txt
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_invalid_entries/input/ 100k_invalid_entries.txt
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_100k_entries/input/ 100k_entries.txt
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_500k_entries/input/ 500k_entries.txt
#python ./src/bryant_testsuite.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_1m_entries/input/ 1m_entries.txt

python ./src/execute.py ./bryants_testsuite/tests/test_easy_median/input/100k_easy_median.txt ./bryants_testsuite/tests/test_easy_median/output/
#python ./src/execute.py ./bryants_testsuite/tests/test_random_amts/input/100k_random_amts.txt ./bryants_testsuite/tests/test_random_amts/output/
#python ./src/execute.py ./bryants_testsuite/tests/test_invalid_entries/input/100k_invalid_entries.txt ./bryants_testsuite/tests/test_invalid_entries/output/
#python ./src/execute.py ./bryants_testsuite/tests/test_100k_entries/input/100k_entries.txt ./bryants_testsuite/tests/test_100k_entries/output/
#python ./src/execute.py ./bryants_testsuite/tests/test_500k_entries/input/500k_entries.txt ./bryants_testsuite/tests/test_500k_entries/output/
#python ./src/execute.py ./bryants_testsuite/tests/test_1m_entries/input/1m_entries.txt ./bryants_testsuite/tests/test_1m_entries/output/

#python ./src/execute.py ./bryants_testsuite/tests/test_1/input/itcont.txt ./bryants_testsuite/tests/test_1/output/