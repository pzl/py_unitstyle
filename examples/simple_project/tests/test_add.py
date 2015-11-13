#!/usr/bin/env python

import unittest
import code

class Add(unittest.TestCase):

	def test_add_numbers(self):
		self.assertEqual(code.add(2,3),5)
		self.assertEqual(code.add(0,0),0)
		self.assertEqual(code.add(-5,5),0)
		self.assertEqual(code.add(-10,4),-6)

	def test_add_strings(self):
		self.assertEqual(code.add("foo","bar"),"foobar")

	def test_raises_adding_mixed_types(self):
		with self.assertRaises(TypeError):
			code.add("foo",3)
