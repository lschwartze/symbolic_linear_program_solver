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
            res = self.a/self.b < other.a/other.b
        res = sp.simplify(res)
        try:
            return bool(res)
        except:
            return res

    def __gt__(self,other):
        res = ""
        if isinstance(other, (int, float)):
            res =  self.a/self.b > other
        else:
            res = self.a/self.b > other.a/other.b
        res = sp.simplify(res)
        try:
            return bool(res)
        except:
            return res
    
    def __rlt__(self,other):
        return self>other
    
    def __rgt__(self,other):
        return self<other