#!/usr/bin/env python

import unittest
import code

#for testing specific assertions
import warnings
import logging

import sys #to get python version, skip new unittest features
import time #simulate slow tests

class GoesAsPlanned(unittest.TestCase):
	""" These tests will all equate to 'passing'
		so they will:
		pass
		expectedFailure and fail
		assertRaises and then raise
		etc
	"""


	def test_should_pass(self):
		self.assertEqual(5,5)

	@unittest.expectedFailure
	def test_expected_failure(self):
		self.assertEqual(4,5)

	@unittest.expectedFailure
	def test_expected_failure_direct_call(self):
		self.fail("I planned to do that")

	def test_raises(self):
		with self.assertRaises(TypeError):
			raise TypeError

	#decorator not for variety here, but for new feature detection
	@unittest.skipIf(sys.version_info[0] < 3 or sys.version_info[1] < 2,"assertWarns was added in Python 3.2, you're running %d.%d" % (sys.version_info[0],sys.version_info[1]))
	def test_warns(self):
		with self.assertWarns(Warning): #python 3.2+
			warnings.warn("foo")

	#decorator not for variety here, but for new feature detection
	@unittest.skipIf(sys.version_info[0] < 3 or sys.version_info[1] < 4,"assertLogs was added in Python 3.4, you're running %d.%d" % (sys.version_info[0],sys.version_info[1]))
	def test_logs(self):
		with self.assertLogs('foo',level="INFO"):
			logging.getLogger('foo').info('message')

	def test_slow_test(self):
		time.sleep(0.5)
		pass


class UnplannedFailures(unittest.TestCase):
	""" These tests are all various failure cases. they will:
		fail
		raise
		expectedFailure and then pass
		assertRaises and pass
		assertRaises and raise something else
	"""

	def test_fails(self):
		self.assertEqual(4,5)

	def test_fails_directly(self):
		self.fail("Manual func call to fail()")


	def test_raises(self):
		raise TypeError

	@unittest.expectedFailure
	def test_expected_failure(self):
		self.assertEqual(2,2)

	def test_expected_raise_and_passes(self):
		with self.assertRaises(TypeError):
			pass

	def test_expected_typeError(self):
		with self.assertRaises(TypeError):
			raise SystemError

	@unittest.skipIf(sys.version_info[0] < 3 or sys.version_info[1] < 2,"assertWarns was added in Python 3.2, you're running %d.%d" % (sys.version_info[0],sys.version_info[1]))
	def test_expected_warn_and_passes(self):
		with self.assertWarns(Warning):
			pass

	@unittest.skipIf(sys.version_info[0] < 3 or sys.version_info[1] < 4,"assertLogs was added in Python 3.4, you're running %d.%d" % (sys.version_info[0],sys.version_info[1]))
	def test_expected_log_wrong_level(self):
		with self.assertLogs('foo',level='INFO'):
			logging.getLogger('foo').debug('message')


class VariousSkips(unittest.TestCase):
	""" These tests will all be skipped in various ways"""

	@unittest.skip("reason for skipping")
	def test_skipped_via_decorator(self):
		pass

	@unittest.skipIf(2 < 3, "reason for skipping")
	def test_skipped_via_skipif(self):
		pass

	@unittest.skipUnless(2 > 3, "reason for skipping")
	def test_skipped_via_skipunless(self):
		pass

	def test_skipped_via_exception(self):
		raise unittest.SkipTest("reason for skipping")

	def test_skipped_via_func(self):
		self.skipTest("reason for skipping")