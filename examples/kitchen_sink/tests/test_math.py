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
