# from django.test import TestCase
import unittest
from fractions import Fraction

# Create your tests here.
class SumTest(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "should be 6")

    def test_list_fraction(self):
        data = [Fraction(1,4), Fraction(1,4), Fraction(2,5)]
        result = sum(data)

    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):
            result = sum(data)

if __name__ == "__main__":
    unittest.main()