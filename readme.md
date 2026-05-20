## A symbolic simplex implementation in Python

Online solvers for linear programs require numbers as input. Sometimes however, one may be interested in the optimal solution to a linear program depending on one or more constants that are a priori unknown. I was not able to find a solver that can deal with this kind of symbolic inputs.

LP_solver implements the simplex algorithm. Input is a standard tableau.
symbolic_fraction implements a class similar to Python's <code> fractions </code>. Essentially, floating point errors can have a huge impact on whether or not simplex finds a correct solution. Since rounding can lead to all kinds of bad edge cases, I decided to simply work with fractions from the get-go. However, <code> fractions </code> can not deal with sypy's symbolic variables that I use for unknown constants. The class symbolic_fraction fixes that and implements all the very basic arithmetic operations that the simplex algorithm needs to perform on fractions.

This is still very much work in progress.

### next steps
- clean up the simplex algorithm
- change behaviour of arithmetic comparisons of symbolic variables
- easier way to input tableau
- form standard tableau from LP