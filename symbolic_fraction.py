# this is essentially implemented by the package 'fraction'
# this implementation offers fewer methods but works with symbolic variables
import math
import numpy as np
import sympy as sp

class symbolic_fraction:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        
        self.simplify()

    def __str__(self):
        if self.b == 1:
            return f"{self.a}"
        
        if type(self.b) == int or self.b.free_symbols == set():
            if type(self.a) == int or self.a.free_symbols == set():
                return f"{self.a}/{self.b}"
            else:
                return f"({self.a})/{self.b}"
        else:
            if type(self.a) == int or self.a.free_symbols == set():
                return f"{self.a}/({self.b})"
            else:
                return f"({self.a})/({self.b})"

    def __repr__(self):
        return str(self)

    def simplify(self):
        if type(self.a) == int and type(self.b) == int:
            div = math.gcd(self.a,self.b)
            self.a = int(self.a/div)
            self.b = int(self.b/div)
        else:
            div = sp.gcd(self.a,self.b)
            self.a = sp.simplify(self.a/div)
            self.b = sp.simplify(self.b/div)

    def __mul__(self, other):
        res = symbolic_fraction(1,1)
        if isinstance(other, (int, np.int32)):
            res.a = self.a*other
            res.b = self.b
        elif isinstance(other, np.ndarray):
            buf_a = self.a
            buf_b = self.b
            return_list = [symbolic_fraction(buf_a,buf_b)*elem for elem in other]
            return np.array(return_list)
        else:
            res.a = self.a*other.a
            res.b = self.b*other.b
        res.simplify()
        return res
    
    def __rmul__(self, other):
        return self*other
    
    def __truediv__(self, other):
        res = symbolic_fraction(1,1)
        if isinstance(other, (int, np.int32)):
            res.b = self.b*other
            res.a = self.a
        else:
            res.a = self.a*other.b
            res.b = self.b*other.a
        res.simplify()
        return res
    
    def __rtruediv__(self, other):
        return other*symbolic_fraction(self.b,self.a)
    
    def __add__(self, other):
        res = symbolic_fraction(1,1)
        if isinstance(other, (int, np.int32)):
            other_as_frac = symbolic_fraction(other,1)
            return self+other_as_frac
        
        if type(self.b) == int and type(other.b) == int:
            fac = math.lcm(self.b, other.b)
            res.a = int(fac/self.b*self.a+fac/other.b*other.a)
            res.b = fac
            res.simplify()
            return res
        else:
            fac = sp.lcm(self.b, other.b)
            res.a = fac/self.b*self.a+fac/other.b*other.a
            res.b = fac
            res.simplify()
            return res
    
    def __radd__(self, other):
        return self+other
        
    def __sub__(self, other):
        return self+(-1)*other
    
    def __rsub__(self,other):
        return other+(-1)*self

    def __lt__(self,other):
        res = ""
        if isinstance(other, (int, float)):
            res =  self.a/self.b < other
        else:
            res = self.a/self.b < other.a*other.b
        res = sp.simplify(res)
        try:
            return bool(res)
        except:
            add_restriction = input(f"add {res} as restriction? [y/n] ")
            while not add_restriction in ["y","n"]:
                add_restriction = input(f"add {sp.simplify(res)} as restriction? [y/n] ")
            return add_restriction == "y"

    def __gt__(self,other):
        if isinstance(other, (int, float)):
            return self.a>other*self.b
        return self.a*other.b > other.a*self.b
    
    def __rlt__(self,other):
        return self>other
    
    def __rgt__(self,other):
        return self<other
    
'''sf_1 = symbolic_fraction(12,8)
sf_2 = symbolic_fraction(8,12)
print(sf_1)
print(sf_2)
print(15*sf_1)
print(sf_2*15)
print(sf_1*sf_2)
print("\n")

sf_3 = symbolic_fraction(45,7)
sf_4 = symbolic_fraction(18,8)
print(sf_3/sf_4)
print(sf_4/18)
print(8/sf_4)
print("\n")

sf_5 = symbolic_fraction(1,2)
sf_6 = symbolic_fraction(1,2)
print(sf_5+sf_6)
print(sf_6+1)
print(1+sf_6)
print("\n")

sf_7 = symbolic_fraction(5,6)
sf_8 = symbolic_fraction(4,2)
print(sf_7-sf_8)
print(1-sf_7)
print("\n")

print(sf_7)
print(sf_6)
print(sf_7<sf_6)
print(sf_6<sf_7)
print(sf_7>sf_6)
print(sf_6>sf_7)


l = [symbolic_fraction(x,3) for x in range(5)]
print(l)

x = np.array(list(range(1,5)))
y = symbolic_fraction(4,3)
print(y*x)

n = sp.Symbol("n", positive = True)
m = sp.Symbol("m", negative = True)
x = symbolic_fraction(2,3)
y = symbolic_fraction(4*n,5*m)
z = symbolic_fraction(1*m,3)
print(x*y)
print(x*z)
print(y*z)
print(2+x)
print(x+2)
print(y+2)
print(2+y)
print(z+y)
print(y+z)
print(symbolic_fraction(m,1)+2<0)'''