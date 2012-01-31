import unittest

from parser.calc.base import calc

class TestTypes(unittest.TestCase):
    def test_number(self):
        self.assertEqual(type(calc.parse('42')), long)

    def test_float(self):
        self.assertEqual(type(calc.parse('23.42')), float)

    def test_complex(self):
        self.assertEqual(type(calc.parse('23+42j')), complex)

class TestBasic(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.parse('1 + 2'), 3)
    
    def test_add3(self):
        self.assertEqual(calc.parse('1 + 2 + 3'), 6)

    def test_div(self):
        self.assertEqual(calc.parse('6 / 3'), 2)

    def test_div3(self):
        self.assertEqual(calc.parse('(6 / 3) / 2'), 1)
        self.assertEqual(calc.parse('6 / (3 / 2)'), 6)
        self.assertEqual(calc.parse('6 / 3 / 2'), 1)

    def test_mod(self):
        self.assertEqual(calc.parse('7 % 3'), 1)

    def test_mod3(self):
        self.assertEqual(calc.parse('21 % 8 % 3'), 2)

    def test_mul(self):
        self.assertEqual(calc.parse('2 * 3'), 6)

    def test_mul3(self):
        self.assertEqual(calc.parse('2 * 3 * 4'), 24)

    def test_sub(self):
        self.assertEqual(calc.parse('1 - 2'), -1)

    def test_sub3(self):
        self.assertEqual(calc.parse('1 - 2 - 3'), -4)


class TestConst(unittest.TestCase):
    def test_e(self):
        self.assertTrue(calc.parse('e') > 2.71)

    def test_pi(self):
        self.assertTrue(calc.parse('pi') > 3.14)


class TestFunc(unittest.TestCase):
    def test_log(self):
        self.assertEqual(calc.parse('log(e)'), 1.0)

    def test_cos(self):
        self.assertEqual(calc.parse('cos(0.0)'), 1.0)
        self.assertEqual(calc.parse('cos(pi)'), -1.0)

    def test_sin(self):
        self.assertEqual(calc.parse('sin(0.0)'), 0.0)

    def test_sqrt(self):
        self.assertEqual(calc.parse('sqrt(16)'), 4)

if __name__ == '__main__':
    unittest.main()

