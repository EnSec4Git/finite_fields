from polynomial import Polynomial
import math
from random import seed, randint
import numbers
seed()


# Code for inversion lazily translated from Wikipedia

def invert_mod_n(x, n):
    if x == 0:
        return None
    t=0; newt=1
    r=n; newr=x
    while newr != 0:
        quotient = r // newr
        (t, newt) = (newt, t - quotient * newt)
        (r, newr) = (newr, r - quotient * newr)
    if r > 1:
        return None
    if t < 0:
        t += n
    return t

def invert_mod_f(x, f):
    if x == 0:
        return None
    #t=polynomial.Polynomial([0]); newt=polynomial.Polynomial([1])
    t=0; newt=1
    r=f; newr=x
    while newr != 0:
        quotient = r // newr
        (t, newt) = (newt, t - quotient * newt)
        (r, newr) = (newr, r - quotient * newr)
    if r.degree() > 0:
        return None
    return t * (1 / r.coef[0])

def naive_factor(n):
    i = 2; limit = int(math.sqrt(n))
    factors = []
    while i <= limit:
        j = 0
        while n % i == 0:
            n /= i
            j += 1
            limit = int(math.sqrt(n))
        if j > 0:
            factors.append((i, j))
        i += 1
    if n != 1:
        factors.append((n, 1))
    return factors

def poly_gcd(f, g):
    if g.degree() > f.degree():
        (f, g) = (g, f)
    while g != 0:
        h = f // g
        (f, g) = (g, f - h * g)
    return f

def is_polynomial_irreducible(poly):
    n = poly.degree()
    if n <= 0:
        return False
    p = poly.coef[0].p
    fc = naive_factor(n)
    for i in range(len(fc)):
        n_i = n / fc[i][0]
        # WARNING: Slow implementation ahead
        pol_i = Polynomial([0, -1] + [0] * (p ** n_i - 2) + [1])
        g = poly_gcd(poly, pol_i)
        if g.degree() > 0:
            return False
    pol_n = Polynomial([0, -1] + [0] * (p ** n - 2) + [1])
    if pol_n % poly != 0:
        return False
    return True

def root_of_polynomial(poly, retries = 100):
    n = poly.degree()
    if n <= 0:
        return None
    field = poly.coef[0].field
    p = field.p
    q = field.q
    s = lambda ls: Polynomial(map(lambda x: field.const(x), ls))
    p1 = s([0, -1] + [0] * (q - 2) + [1])
    f1 = poly_gcd(p1, poly)
    if f1.degree() < 1:
        return None
    return root_of_separable(f1)

def root_of_separable(poly, retries = 100):
    # Cantor-Zassenhaus algorithm
    n = poly.degree()
    if n < 1:
        return None
    elif n == 1:
        return (- poly.coef[0]) / poly.coef[1]
    ff = poly.coef[0].field
    p = ff.p
    q = ff.q
    n1 = ff.f.degree()
    found_poly = False
    while not found_poly and retries > 0:
        r = Polynomial([ff.element_from_polynomial(Polynomial([randint(0, p-1) for i in range(n1)])) for j in range(n)])
        # WARNING: Very slow implementation, fix soon
        #s = (r ** ((p-1)/2)) % poly
        s = r.power((p-1)/2, poly)
        p1 = poly_gcd(s + 1, poly)
        retries -= 1
        found_poly = p1.degree() > 0 and p1.degree() < n
    if retries == 0:
        return None
    return root_of_separable(p1)

class NumberModuloP(object):
    def __lift(self, x):
        if isinstance(x, NumberModuloP):
            assert self.p == x.p
            return x
        elif isinstance(x, numbers.Number):
            return NumberModuloP(x, self.p)
        else:
            return NotImplemented
    
    def __init__(self, n, p):
        self.p = p
        self.n = n % p
    
    def __add__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return NumberModuloP(self.n + y.n, self.p)
    
    def __sub__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return NumberModuloP(self.n - y.n, self.p)
    
    def __mul__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return NumberModuloP(self.n * y.n, self.p)
    
    def __div__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return NumberModuloP(self.n * invert_mod_n(y.n, y.p), self.p)
    
    def __floordiv__(self, x):
        return self / x
    
    def __eq__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return self.n == y.n
    
    def __ne__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return self.n != y.n
    
    def __neg__(self):
        return NumberModuloP(-self.n, self.p)
    
    def __radd__(self, x):
        return NumberModuloP(self.n + x, self.p)
    
    def __rsub__(self, x):
        return NumberModuloP(x - self.n, self.p)
    
    def __rmul__(self, x):
        return NumberModuloP(self.n * x, self.p)
    
    def __rdiv__(self, x):
        return NumberModuloP(x * invert_mod_n(self.n, self.p), self.p)
    
    def __rfloordiv__(self, x):
        return NumberModuloP(x, self.p) // self
    
    def __pow__(self, e):
        return NumberModuloP(pow(self.n, e, self.p), self.p)
    
    def __repr__(self):
        #return "{0} % {1}".format(self.n, self.p)
        return str(self.n)

class FFElement(object):
    def __lift(self, x):
        if isinstance(x, FFElement):
            assert self.field == x.field
            return x
        elif isinstance(x, NumberModuloP):
            assert self.field.p == x.p
            return self.field.const(x.n)
        elif isinstance(x, numbers.Number):
            return self.field.const(x)
        else:
            return NotImplemented
    
    def __init__(self, field, val):
        self.x = val
        self.field = field
    
    def __add__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return FFElement(self.field, (self.x + y.x) % self.field.f)
    
    def __sub__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return FFElement(self.field, (self.x + self.field.f - y.x) % self.field.f)
    
    def __mul__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return FFElement(self.field, (self.x * y.x) % self.field.f)
    
    def __neg__(self):
        return FFElement(self.field, Polynomial(map(lambda x: -x, self.x.coef)))
    
    def __div__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return self * FFElement(self.field, invert_mod_f(y.x, self.field.f))
    
    def __floordiv__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return self / y
    
    def __eq__(self, x):
        try:
            y = self.__lift(x)
            if y == NotImplemented: return y
        except AssertionError:
            return False
        return self.x == y.x
    
    def __radd__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return self + y
    
    def __rsub__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return y - self
    
    def __rmul__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return y * self
    
    def __rdiv__(self, x):
        y = self.__lift(x)
        if y == NotImplemented: return y
        return y / self
    
    def __pow__(self, n):
        res = self.field.one()
        n1 = n
        q = self
        while n1 > 0:
            if n1 % 2 != 0:
               res = res * q
            n1 /= 2
            q = q * q
        return res
    
    def __repr__(self):
        return "{0}_{1}".format(repr(self.x), self.field.p)

class FiniteField(object):
    def __init__(self, poly, p):
        self.p = p
        makemodp = lambda t: t if isinstance(t, NumberModuloP) else NumberModuloP(t, self.p)
        self.f = Polynomial(map(lambda x: makemodp(x), poly.coef))
        self.q = pow(p, poly.degree())
        if not is_polynomial_irreducible(self.f):
            raise ValueError("The polynomial provided is not irreducible")
    
    @staticmethod
    def of_size(q, p=None):
        if p == None:
            # WARNING: SLOW CODE AHEAD
            (p, n) = naive_factor(q)[0];
        else:
            n = 0
            q1 = q
            while q1 % p == 0:
                q1 /= p
                n += 1
            if q1 != 1: raise ValueError("q should be equal to p^n for some n")
        found_poly = False
        while not found_poly:
            # WARNING: BIASED RANDOM GENERATOR BELOW
            poly = Polynomial([NumberModuloP(randint(0, p-1), p) for i in range(n + 1)])
            if poly.degree() == n:
                found_poly = is_polynomial_irreducible(poly)
        return FiniteField(poly, p)
    
    def zero(self):
        return FFElement(self, Polynomial([NumberModuloP(0, self.p)]))
    
    def one(self):
        return FFElement(self, Polynomial([NumberModuloP(1, self.p)]))
    
    def const(self, c):
        return FFElement(self, Polynomial([NumberModuloP(c, self.p)]))
    
    def element_from_polynomial(self, p):
        m = lambda t: map(lambda x: NumberModuloP(x, self.p), t)
        return FFElement(self, Polynomial(m(p.coef)))
    
    def is_isomorphic_to(self, other):
        return self.q == other.q
    
    def isomorphism_to(self, other):
        assert self.q == other.q
        assert self.p == other.p
        x1 = Polynomial(map(lambda x: other.const(x.n), self.f.coef))
        rt = root_of_polynomial(x1)
        #print rt
        if rt is None:
            raise Error("Could not find root of polynomial in the other field: " + x1)
        def image(elem):
            if elem.field != self:
                raise ValueError("Image of non-element is not defined")
            p = elem.x
            res = other.zero()
            for (i, c) in enumerate(p.coef):
                res = res + c * (rt ** i)
            return res
        return image
    
    def __repr__(self):
        return "Z_{0}[x]/({1}) ~= Z_{2}".format(self.p, self.f, self.q)
    
    def __eq__(self, x):
        return self.p == x.p and self.f == x.f