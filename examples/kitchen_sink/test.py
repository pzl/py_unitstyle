#!/usr/bin/env python

import sys #to get argument
import unittest
import unitstyle


#collect all of our test scripts as a test suite
my_tests = unittest.TestLoader().discover("tests/")

# get command-line output format if provided
try:
	output_format = sys.argv[1]
except IndexError:
	#nothing provided
	output_format = ''

#run our test suite using unitstyle
unitstyle.TestRunner(format=output_format).run(my_tests)
