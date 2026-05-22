import LP_solver as lp
import sympy as sp
import symbolic_fraction as sb
import numpy as np
from pprint import pprint

n = sp.Symbol("n", finite=True)
m = sp.Symbol("m", positive=True, finite=True)
matrix = np.array(
                [[0, 0, 0, 0, -1, -1, -2, 0],
                [1, 0, 0, 0, 1, 0, 1, 6],
                [0, 1, 0, 0, 0, 1, 1, n],
                [0, 0, 1, 0, 0, 3, -1, 6],
                [0, 0, 0, 1, m, 0, 0, 3]],
            dtype=object)

matrix = np.array([[sb.symbolic_fraction(x,1) for x in l] for l in matrix])
restrictions = dict()

# This is a callback function that allows us to access the matrix after every
# modification step in the simplex algorithm. This works because the simplex function implements
# logic for a callback
def show_data(data="", prompt=""):
    if data!="":
        if type(data) == str:
            print(data)
        else:
            pprint(data.matrix)
        return None
    if prompt!="":
        return input(prompt)

if __name__ == '__main__':
    prog = lp.LP_solver(matrix)
    prog.simplex(show_data)