import copy

class InfiniteArray(object):
    def __init__(self, arr):
        if isinstance(arr, InfiniteArray):
            self._array = copy.copy(arr._array)
        else:
            self._array = copy.copy(arr)
    
    def __getitem__(self, index):
        if index >= len(self._array):
            return 0
        return self._array[index]
    
    def __len__(self):
        while len(self._array) and self._array[-1] == 0:
            self._array = self._array[:-1]
        return len(self._array)
    
    def __setitem__(self, index, value):
        l = len(self._array)
        if index >= l:
            self._array += [0] * (index - l)
            self._array += [value]
        else:
            self._array[index] = value
    
    def __iter__(self):
        return iter(self._array)
    
    def __repr__(self):
        return "IA: " + repr(self._array)


class Polynomial(object):
    def __init__(self, other):
        if isinstance(other, Polynomial):
            self.coef = InfiniteArray(other.coef)
        else:
            self.coef = InfiniteArray(other)
    
    def degree(self):
        return len(self.coef) - 1
    
    def __add__(self, x):
        result = Polynomial(self.coef)
        if isinstance(x, Polynomial):
            for i in range(len(x.coef)):
                result.coef[i] += x.coef[i]
        else:
            result.coef[0] += x
        return result
    
    def __sub__(self, x):
        result = Polynomial(self.coef)
        if isinstance(x, Polynomial):
            for i in range(len(x.coef)):
                result.coef[i] -= x.coef[i]
        else:
            result.coef[0] -= x
        return result
    
    def __mul__(self, x):
        if isinstance(x, Polynomial):
            result = Polynomial([])
            for i in range(len(self.coef)):
                for j in range(len(x.coef)):
                    result.coef[i+j] += self.coef[i] * x.coef[j]
        else:
            result = Polynomial(map(lambda t: t * x, self.coef))
        return result
    
    def __floordiv__(self, x):
        if isinstance(x, Polynomial):
            result = Polynomial([])
            rem = Polynomial(self.coef)
            while rem.degree() >= x.degree():
                d = rem.degree() - x.degree()
                c = rem.coef[-1] // x.coef[-1]
                for i in range(len(x.coef)):
                    rem.coef[i + d] -= x.coef[i] * c
                result.coef[d] += c
        else:
            result = Polynomial(map(lambda t: t // x, self.coef))
        return result
    
    def __pow__(self, n):
        d = self.degree()
        res = Polynomial([self.coef[d] / self.coef[d]])
        n1 = n
        q = Polynomial(self)
        while n1 > 0:
            if n1 % 2 != 0:
               res = res * q
            n1 /= 2
            q = q * q
        return res
    
    def power(self, degree, modulus = None):
        if modulus == None:
            return self ** degree
        d = self.degree()
        res = Polynomial([self.coef[d] / self.coef[d]])
        n1 = degree
        q = Polynomial(self)
        while n1 > 0:
            if n1 % 2 != 0:
                res = res * q
                res = res % modulus
            n1 /= 2
            q = q * q
            q = q % modulus
        return res
    
    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return self.degree() < 1 and self.coef[0] == other
        if self.degree() != other.degree():
            return False
        for i in range(self.degree() + 1):
            if self.coef[i] != other.coef[i]:
                return False
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __div__(self, x):
        if isinstance(x, Polynomial):
            result = Polynomial([])
            rem = Polynomial(self.coef)
            while rem.degree() >= x.degree():
                d = rem.degree() - x.degree()
                c = rem.coef[-1] / x.coef[-1]
                for i in range(len(x.coef)):
                    rem.coef[i + d] -= x.coef[i] * c
                result.coef[d] += c
        else:
            result = Polynomial(map(lambda t: t / x, self.coef))
        return result
    
    def __mod__(self, x):
        if isinstance(x, Polynomial):
            result = (self - x * (self / x))
        else:
            result = Polynomial(map(lambda t: t % x, self.coef))
        return result
    
    def __radd__(self, x):
        return self.__add__(x)
    
    def __rsub__(self, x):
        return -(self.__sub__(x))
    
    def __rmul__(self, x):
        return self.__mul__(x)
    
    def __neg__(self):
        return Polynomial(map(lambda t: -t, self.coef))
    
    def __repr__(self):
        res = ""
        l = len(self.coef)
        if l == 1 and self.coef[0] == 0 or l == 0:
            return "0"
        for i in range(l):
            if self.coef[i] != 0:
                is_unit = (self.coef[i] == 1)
                if not is_unit or i == 0:
                    res += str(self.coef[i])
                if i != 0:
                    res += ("*" if not is_unit else "") + "x"
                    if i != 1:
                        res += "^" + str(i)
                res += " + "
        return res[:-3]
