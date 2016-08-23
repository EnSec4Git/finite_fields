from finite_field import FiniteField, root_of_polynomial
from polynomial import Polynomial
a = FiniteField(Polynomial([1, 0, -1, 1]), 3)
b = FiniteField(Polynomial([1, -1, 0, 1]), 3)
s = lambda x: a.element_from_polynomial(Polynomial(x))
t = a.isomorphism_to(b)
print t(s([1,0,1,0]))
