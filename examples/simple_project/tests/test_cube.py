#!/usr/bin/env python

import unittest
import code

class Cube(unittest.TestCase):

	def test_cubes_numbers(self):
		self.assertEqual(code.cube(2),8)
		self.assertEqual(code.cube(3),27)
		self.assertEqual(code.cube(0),0)
		self.assertEqual(code.cube(-5),-125)
		self.assertAlmostEqual(code.cube(4.4),85.184) # yay floating point

	def test_raises_cubing_strings(self):
		with self.assertRaises(TypeError):
			code.cube("foo")
