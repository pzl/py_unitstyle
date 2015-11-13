#!/usr/bin/env python

import unittest
import unitstyle


#collect all of our test scripts as a test suite
my_tests = unittest.TestLoader().discover("tests/")

#run our test suite using unitstyle
unitstyle.TestRunner().run(my_tests)
