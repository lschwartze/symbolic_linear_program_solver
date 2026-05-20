import sympy as sp
import numpy as np
import symbolic_fraction as sb
from pprint import pprint

n = sp.Symbol("n", positive = True)
m = sp.Symbol("m", positive=True)
matrix = np.array(
                [[0, 0, 0, 0, -1, -1, -2, 0],
                [1, 0, 0, 0, 1, 0, 1, n], # n=6
                [0, 1, 0, 0, 0, 1, 1, n],
                [0, 0, 1, 0, 0, 3, -1, 2*m],
                [0, 0, 0, 1, 1, 0, 0, m]], # m=3
            dtype=object)

matrix = np.array([[sb.symbolic_fraction(x,1) for x in l] for l in matrix])

pprint(matrix)

n = len(matrix[0])
m = len(matrix)

while np.any(matrix[0]<0):
    j = 0
    for i in range(len(matrix[0])):
        if matrix[0][i]<0:
            j = i
            break

    min_val = np.inf
    l = 0
    solution_exists = False
    for i in range(1,m):
        if matrix[i][j]>0:
            solution_exists=True
            val = matrix[i][-1]/matrix[i][j]
            if val < min_val:
                min_val = val
                l = i
    if not solution_exists:
        print("The program is unbounded!")
        break


    element_to_leave_basis = 0
    for i in range(l):
        if matrix[l][i] > 0:
            element_to_leave_basis = i
            break

    print("leaving index: ", element_to_leave_basis, "\n",
          "j :" , j, "\n",
          "l: ", l)

    pivot_value = matrix[l][j]
    matrix[l] = matrix[l]/pivot_value
    
    pprint(matrix)

    for i in range(m):
        if i == l:
            continue
        add_factor = matrix[i][j]
        matrix[i] = matrix[i] - add_factor*matrix[l]

    pprint(matrix)

    for i in range(m):
        buffer = matrix[i][element_to_leave_basis]
        matrix[i][element_to_leave_basis] = matrix[i][j]
        matrix[i][j] = buffer

    pprint(matrix)

if solution_exists:
    print(f"the optimal value of the linear program is {matrix[0][-1]}")