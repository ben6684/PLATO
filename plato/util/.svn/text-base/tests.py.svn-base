"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

# from django.test import TestCase

# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.failUnlessEqual(1 + 1, 2)

# __test__ = {"doctest": """
# Another way to test that 1 + 1 is equal to 2.

# >>> 1 + 1 == 2
# True
# """}
import unittest

class Test_trans_fr(unittest.TestCase):
	def test_trans_not_in(self):
		"""
		test if with a name is always catch
		"""
		label = 'toto'
		response = trans_fr(label)
		self.assertEqual(response,label)
		self.assertEqual(response,u"Nom de l'outil")
	def test_trans_fr_in(self):
		label="Tool Name"
		response = trans_fr(label)
		self.assertEqual(response,label)
		self.assertEqual(response,u"Nom de l'outil")
		
