import unittest
from polynomial import InfiniteArray, Polynomial
from finite_field import NumberModuloP

class TestInfiniteArrayMethods(unittest.TestCase):
    def test_get(self):
        array = InfiniteArray([1, 2, 3])
        self.assertEqual(array[0], 1)
        self.assertEqual(array[1], 2)
        self.assertEqual(array[2], 3)
        self.assertEqual(array[3], 0)
        self.assertEqual(array[1000], 0)
        self.assertEqual(len(array), 3)

    def test_set(self):
        array = InfiniteArray([1])
        array[5] = 2
        self.assertEqual(array[5], 2)
        self.assertEqual(array[4], 0)
        self.assertEqual(array[6], 0)
        self.assertEqual(len(array), 6)

    def test_length(self):
        array = InfiniteArray([1, 2])
        self.assertEqual(len(array), 2)
        array[2] = 4
        self.assertEqual(len(array), 3)
        array[1000] = 5
        self.assertEqual(len(array), 1001)
        array[1000] = 0
        self.assertEqual(len(array), 3)

class TestPolynomialMethods(unittest.TestCase):
    def test_copy(self):
        a = Polynomial([1])
        b = Polynomial(a.coef)
        a.coef[0] = 2
        self.assertEqual(a.coef[0], 2)
        self.assertEqual(b.coef[0], 1)
    
    def test_add(self):
        a = Polynomial([1, 2])
        b = Polynomial([1, 3])
        c = Polynomial([2, 5])
        self.assertEqual(a + b, c)
    
    def test_sub(self):
        a = Polynomial([0, 1])
        b = Polynomial([2, 4])
        c = Polynomial([-2, -3])
        self.assertEqual(a - b, c)
    
    def test_arith_modp(self):
        b = lambda t: map(lambda x: NumberModuloP(x, 31), t)
        p1 = Polynomial(b([1,1]))
        p2 = Polynomial(b([0,0,1]))
        p3 = Polynomial(b([0,1]))
        p4 = Polynomial(b([1,1,0,-1]))
        ans = p1 - p2*p3
        self.assertEqual(ans, p4)
    
    def test_mul(self):
        a = Polynomial([1, 3])
        b = Polynomial([2, 4, 7])
        c = Polynomial([2, 10, 19, 21])
        self.assertEqual(a * b, c)
    
    def test_div(self):
        a = Polynomial([1, 2, 1])
        b = Polynomial([1, 1])
        self.assertEqual(a / b, b)
        a = Polynomial([1,1,0,1,1,0,0,0,1])
        b = Polynomial([1,1,0,0,1,0,1])
        c = Polynomial([-1, 0, 1])
        self.assertEqual(a / b, c)
    
    def test_mod(self):
        a = Polynomial([1, 3, 4, 2])
        b = Polynomial([1, 1])
        self.assertEqual(a % b, Polynomial([0]))
        c = Polynomial([2, 1])
        #print a / c, ", ", (a - c * (a / c))
        self.assertEqual(a % c, Polynomial([-5]))
    
    def test_pow(self):
        a = Polynomial([1, 1])
        self.assertEqual(a ** 3, Polynomial([1, 3, 3, 1]))
        self.assertEqual(a ** 2, Polynomial([1, 2, 1]))
        b = Polynomial([-1, 1])
        self.assertEqual(b ** 2, Polynomial([1, -2, 1]))
    
    def test_cmp(self):
        a = Polynomial([1, 1])
        b = Polynomial([1, 1])
        self.assertEqual(a, b)
        b.coef[0] = 2
        self.assertNotEqual(a, b)
        c = Polynomial([0, 1]) + Polynomial([1, 0])
        self.assertEqual(c, a)
        self.assertEqual(Polynomial([]), Polynomial([0]))

if __name__ == '__main__':
    unittest.main()