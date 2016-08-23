import unittest
from finite_field import invert_mod_f, invert_mod_n, NumberModuloP, FiniteField, poly_gcd, is_polynomial_irreducible
from polynomial import Polynomial

class TestInversionModNF(unittest.TestCase):
    def test_number_inversion(self):
        self.assertEqual(invert_mod_n(3, 26), 9)
        self.assertEqual(invert_mod_n(3, 8), 3)
        self.assertNotEqual(invert_mod_n(3, 8), 5)
    
    def test_polynomial_inversion(self):
        self.assertEqual(invert_mod_f(Polynomial([0,1]), Polynomial([1,1,1])), Polynomial([-1,-1]))
        # a = 1 + x + x^4 + x^6, f = 1 + x + x^3 + x^4 + x^8, result = x + x^3 + x^6 + x^7
    
    def test_polynomial_inversion_over_Zq(self):
        b = lambda t: map(lambda x: NumberModuloP(x, 2), t)
        self.assertEqual(invert_mod_f(Polynomial(b([1,1,0,0,1,0,1])), \
            Polynomial(b([1,1,0,1,1,0,0,0,1]))), \
            Polynomial(b([0,1,0,1,0,0,1,1])))
    
    def test_polynomial_inversion_over_Zq2(self):
        b = lambda t: map(lambda x: NumberModuloP(x, 31), t)
        p1 = Polynomial(b([-1, 1, 1, 0, -1, 0, 1, 0, 0, 1, -1]))
        p2 = Polynomial(b([-1] + [0] * 10 + [1]))
        p3 = Polynomial(b([9, 5, 16, 3, 15, 15, 22, 19, 18, 29, 5]))
        self.assertEqual(invert_mod_f(p1, p2), p3)

class TestPolyGcd(unittest.TestCase):
    def setUp(self):
        h = lambda x: NumberModuloP(x, 3)
        self.t = lambda u: Polynomial(map(h, u))
    
    def assertEqualPoly(self, p1, p2):
        self.assertNotEqual(p1 // p2, 0)
        self.assertNotEqual(p2 // p1, 0)
    
    def test_gcd1(self):
        p1 = self.t([-1, 0, 1])
        p2 = self.t([-1, 1])
        gcd = poly_gcd(p1, p2)
        self.assertEqualPoly(gcd, p2)
    
    def test_gcd2(self):
        p1 = self.t([1, 2, 1])
        p2 = self.t([-1, 0, 1])
        p3 = self.t([1, 1])
        self.assertEqualPoly(poly_gcd(p1, p2), p3)
    
    def test_gcd3(self):
        p1 = self.t([1, 0, 1])
        p2 = self.t([0, 1])
        self.assertEqualPoly(poly_gcd(p1, p2), self.t([1]))

class TestPolynomialIrreducibility(unittest.TestCase):
    def setUp(self):
        metat = lambda p: lambda u: Polynomial(map(lambda x: NumberModuloP(x, p), u))
        self.t = metat(3)
        self.s = metat(2)
    
    def testPoly1(self):
        p = self.t([1, 0, 2, 1])
        self.assertTrue(is_polynomial_irreducible(p))
    
    def testPoly2(self):
        p = self.t([1,1,0,0,1])
        self.assertFalse(is_polynomial_irreducible(p))
    
    def testPoly2(self):
        p = self.s([1,1,0,0,1])
        self.assertTrue(is_polynomial_irreducible(p))
    
    def testPoly3(self):
        p = self.s([1,0,0,1,1])
        self.assertTrue(is_polynomial_irreducible(p))

class TestOfSizeMethod(unittest.TestCase):
    def assertSanePoly(self, poly, p):
        self.assertEqual(poly.p, p)
        self.assertTrue(is_polynomial_irreducible(poly.f))

    def test_size1(self):
        p = FiniteField.of_size(25, 5)
        self.assertSanePoly(p, 5)
    
    def test_size2(self):
        p = FiniteField.of_size(27, 3)
        self.assertSanePoly(p, 3)
    
    def test_size3(self):
        p = FiniteField.of_size(16, 2)
        self.assertSanePoly(p, 2)


class TestRijndaelFiniteField(unittest.TestCase):
    def setUp(self):
        poly = Polynomial([1, 1, 0, 1, 1, 0, 0, 0, 1])
        self.field = FiniteField(poly, 2)
    
    def test_multiplication(self):
        #b = lambda t: map(lambda x: NumberModuloP(x, 2), t)
        a = self.field.element_from_polynomial(Polynomial([1, 1, 0, 0, 1, 0, 1]))
        b = self.field.element_from_polynomial(Polynomial([0, 1, 0, 1, 0, 0, 1, 1]))
        c = self.field.element_from_polynomial(Polynomial([1]))
        self.assertEqual(a * b, c)
    
    def test_addition(self):
        pass

if __name__ == '__main__':
    unittest.main()