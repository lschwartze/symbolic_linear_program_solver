import sympy as sp
import numpy as np
import symbolic_fraction as sb
from pprint import pprint

n = sp.Symbol("n")
m = sp.Symbol("m", positive=True)
matrix = np.array(
                [[0, 0, 0, 0, -1, -1, -2, 0],
                [1, 0, 0, 0, 1, 0, 1, 6],
                [0, 1, 0, 0, 0, 1, 1, n],
                [0, 0, 1, 0, 0, 3, -1, 6],
                [0, 0, 0, 1, 1, 0, 0, 3]],
            dtype=object)

matrix = np.array([[sb.symbolic_fraction(x,1) for x in l] for l in matrix])
restrictions = dict()

def is_optimum(matrix, restrictions): # checks whether the current value is optimal
    for e in matrix[0]:
        rel = e<0
        truthy,restrictions = comparison(rel, restrictions)
        if truthy:
            return False, restrictions
    return True, restrictions

def comparison(rel, restrictions):
    '''
    Since we are working with symbolic variables and the class symbolic_fraction overwrites the
    operators < and >, we have to be careful about comparisons.
    The comparison operators have two different return types:
    - bool: In this case both sides of the comparison are fractions involving only numbers.
            The operator definition in symbolic_fraction determines the truth-value of the 
            comparison and returns the boolean.
    - relation: In this case at least one of the sides of the comparison involves a 
                symbolic variable. Example: Suppose we query (-1)*n+2<3. The return-value is then
                the simplified expression n>1. 
    To continue, the simplex algorithm requires input from the user, whether this should be
    accepted as true or not. If the user accepts this restriction, the function comparison returns
    True. If the user does not accept, the function returns False. 
    Note: At every point the user has to decide for exactly one of the options. If for example,
    n>1 is not accepted, the program will automatically accept n<=1. If the values of n could be
    any integer, then the user would have to run the algorithm twice to compute a solution for 
    each of the options.
    Accepted relations will also be stored in a dictionary which the function will consult to 
    determine the validity of future relations.
    '''
    if type(rel) == bool:
        return rel, restrictions
    else:
        if rel in restrictions:
            return restrictions[rel], restrictions
        add_restriction = input(f"add {rel} as restriction? [y/n] ")
        while not add_restriction in ["y","n"]:
            add_restriction = input(f"add {sp.simplify(rel)} as restriction? [y/n] ")
        restrictions[rel] = add_restriction=="y"
        return restrictions[rel], restrictions

def simplex(matrix, restrictions):
    pprint(matrix)

    m = len(matrix)

    truthy,restrictions = is_optimum(matrix, restrictions)
    while not truthy: # negative values in objective -> improvement possible
        j = 0
        for i in range(len(matrix[0])): # Bland's rule: pick negative entry of smallest index
            rel = matrix[0][i]<0
            truthy, restrictions = comparison(rel, restrictions)
            if truthy:
                j = i
                break

        min_val = np.inf
        l = 0
        solution_exists = False
        for i in range(1,m): # also Bland's rule: pick row such that ratio is minimum.
            rel = matrix[i][j]>0
            truthy, restrictions = comparison(rel, restrictions)
            if truthy:
                solution_exists=True
                val = matrix[i][-1]/matrix[i][j]
                rel = val < min_val
                truthy, restrictions = comparison(rel, restrictions)
                if truthy: # among all rows with minimum ratio, pick smallest index one
                    min_val = val
                    l = i
        if not solution_exists: # if no positive value in pivot column, program is unbounded
            print("The program is unbounded!")
            break

        # since the tableau has an identity matrix at the start, the leaving variable is 
        # associated with the first non-zero column of the pivot row
        element_to_leave_basis = 0
        for i in range(l):
            rel = matrix[l][i] > 0
            truthy, restrictions = comparison(rel, restrictions)
            if truthy:
                element_to_leave_basis = i
                break

        print("leaving index: ", element_to_leave_basis, "\n",
            "j :" , j, "\n",
            "l: ", l)

        # normalize pivot row
        pivot_value = matrix[l][j]
        matrix[l] = matrix[l]/pivot_value
        
        pprint(matrix)

        # turn pivot column into unit vector
        for i in range(m):
            if i == l:
                continue
            add_factor = matrix[i][j]
            matrix[i] = matrix[i] - add_factor*matrix[l]

        pprint(matrix)

        # rearrange columns such that tableau begins with identity matrix
        for i in range(m):
            buffer = matrix[i][element_to_leave_basis]
            matrix[i][element_to_leave_basis] = matrix[i][j]
            matrix[i][j] = buffer

        pprint(matrix)

        truthy,restrictions = is_optimum(matrix, restrictions)

    if solution_exists:
        print(f"the optimal value of the linear program is {matrix[0][-1]}")


if __name__ == '__main__':
    simplex(matrix, restrictions)