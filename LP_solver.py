import sympy as sp
import numpy as np

class LP_solver:

    def __init__(self, matrix, restrictions = dict()):
        self.matrix = matrix
        self.restrictions = restrictions


    def is_optimum(self): # checks whether the current value is optimal
        for e in self.matrix[0]:
            rel = e<0
            truthy = self.comparison(rel)
            if truthy:
                return False
        return True

    def comparison(self, rel, callback=None):
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
        try:
            return bool(rel)
        except:
            if rel in self.restrictions: # rel was considered earlier already
                return self.restrictions[rel]
            if ~rel in self.restrictions: # negation of rel was considered earlier already
                return self.restrictions[~rel]
            
            follows = self.follows_from_restrictions(rel) # do current restrictions imply rel
            if type(follows) == dict:
                return follows[rel]

            if callback:
                add_restriction = callback(prompt = f"add {rel} as restriction? [y/n] ")
            while not add_restriction in ["y","n"]:
                add_restriction = callback(prompt = f"add {sp.simplify(rel)} as restriction? [y/n] ")
            self.restrictions[rel] = add_restriction=="y"
            return self.restrictions[rel]
    
    def follows_from_restrictions(self, rel):
        if len(list(rel.free_symbols)) > 1: # Currently no handling for relations with more symbols
            return False
        solution_set = 1<=1
        num_compatible_restrictions = 0
        for ineq in self.restrictions: # combine all relevant known restrictions
            if ineq.free_symbols == rel.free_symbols:
                if self.restrictions[ineq]:
                    solution_set = sp.And(solution_set, ineq)
                else:
                    solution_set = sp.And(solution_set, ~ineq)
                num_compatible_restrictions+=1
        
        if num_compatible_restrictions==0: # no previous restrictions can be used
            return False

        solution_set = solution_set.as_set()
        rel_set = rel.as_set()
        not_rel_set = (~rel).as_set()

        if solution_set.is_subset(rel_set):
            return {rel: True} # new relation must be true
        if solution_set.is_subset(not_rel_set):
            return {rel: False} # new relation must be false
        return False
    

    def simplex(self, callback=None):
        if callback:
            callback(self)

        m = len(self.matrix)

        truthy = self.is_optimum()
        while not truthy: # negative values in objective -> improvement possible
            j = 0
            for i in range(len(self.matrix[0])): # Bland's rule: pick negative entry of smallest index
                rel = self.matrix[0][i]<0
                truthy = self.comparison(rel, callback)
                if truthy:
                    j = i
                    break

            min_val = np.inf
            l = 0
            solution_exists = False
            for i in range(1,m): # also Bland's rule: pick row such that ratio is minimum.
                rel = self.matrix[i][j]>0
                truthy = self.comparison(rel, callback)
                if truthy:
                    solution_exists=True
                    val = self.matrix[i][-1]/self.matrix[i][j]
                    rel = val < min_val
                    truthy = self.comparison(rel, callback)
                    if truthy: # among all rows with minimum ratio, pick smallest index one
                        min_val = val
                        l = i
            if not solution_exists and callback: # if no positive value in pivot column, program is unbounded
                callback("The program is unbounded!")
                break

            # since the tableau has an identity matrix at the start, the leaving variable is 
            # associated with the first non-zero column of the pivot row
            element_to_leave_basis = 0
            for i in range(l):
                rel = self.matrix[l][i] > 0
                truthy = self.comparison(rel, callback)
                if truthy:
                    element_to_leave_basis = i
                    break
            
            if callback:
                callback(f"leaving index: {element_to_leave_basis}, \nj : {j}, \nl: {l}")

            # normalize pivot row
            pivot_value = self.matrix[l][j]
            self.matrix[l] = self.matrix[l]/pivot_value
            
            if callback:
                callback(self)

            # turn pivot column into unit vector
            for i in range(m):
                if i == l:
                    continue
                add_factor = self.matrix[i][j]
                self.matrix[i] = self.matrix[i] - add_factor*self.matrix[l]

            if callback:
                callback(self)

            # rearrange columns such that tableau begins with identity matrix
            for i in range(m):
                buffer = self.matrix[i][element_to_leave_basis]
                self.matrix[i][element_to_leave_basis] = self.matrix[i][j]
                self.matrix[i][j] = buffer

            if callback:
                callback(self)

            truthy = self.is_optimum()

        if solution_exists and callback:
            callback(f"the optimal value of the linear program is {self.matrix[0][-1]}")