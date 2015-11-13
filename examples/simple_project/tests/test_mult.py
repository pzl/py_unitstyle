#!/usr/bin/env python

import unittest
import code

class Multiply(unittest.TestCase):

	def test_mult_numbers(self):
		self.assertEqual(code.multiply(2,3),6)
		self.assertEqual(code.multiply(0,0),0)
		self.assertEqual(code.multiply(-1,5),-5)
		self.assertAlmostEqual(code.multiply(5.5,1.1),6.05)

	def test_duplicates_strings(self):
		self.assertEqual(code.multiply("foo",3),"foofoofoo")

	def test_raises_multiplying_two_strings(self):
		with self.assertRaises(TypeError):
			code.multiply("foo","bar")
