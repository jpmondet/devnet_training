# Algebra

## Vector

Ordered set of n elements with n dimensions. Elements may be unrelated

### Addition

- Only between vectors of same dimension.
- Inherits properties of the element's field

### Transpose 

- Denoted x^T
- row vector becomes column vector and vice versa

### Multiplication

- Scaling -> the vector becomes the vector where each elements are multiplied by the scalar
- Multiplying 2 vectors (dot product): s = x.y = SUM(xi * yi) for i = 1 to n (which is a scalar!)


## Matrix

- Set of vectors
- m x n matrix = m rows, n columns
- elements of a column are generally related to each other

### Addition

- Defined only for matrixes of same number of rows and same number of columns
- Inherits properties of the element's field

### Transpose 

If A is mxn matrix, A^T is nxm matrix

### Multiplication

- Scaling (same as vector)
- Product of matrices:

If C = AB, cij = SUM(aik * bkj) for k=1 to n 

/!\ The number of columns (dimension of each row) in A must equal the number of rows (dimension of each column) of B !!

-> mxn matrix multiplied by nxc matrix  = mxc matrix

 - associative
 - NOT commutative

### Exponential 

If A is a square matrix, then e^A = I + A + A^2/2! + ...

## Field

A field is a (in)finite set that supports the operations of addition and
multiplication on elements of this set. Also satifies : 
- Closure (for a, b in F, if a+b=c and a * b = d, then c,d are also in F)
- Commutativity
- Associativity
- Identity (0 for addition & 1 for multiplication)
- Inverses
- Distributivity

## Linear Combination

k real-valued variables x1,..., xk and k real-valued variables w1, ... , wk 

-> s = x1w1 + x2w2 + ... xkwk is the linear combination of the variables.

(same for vectors)

## Linear Independence

Vectors are independent if we can't express a vector as a linear combination of the others.

More formally, the matrix formed by the vectors is non-singular (has a non-zero determinant)

## Basis

In a set of vectors, the basis is formed by the subset of vectors that are linearly independent (thus we can derive the other vectors from them)

## Vector space

Set of vector formed by the basis (which can be an infinite set)

## Dimension

Cardinality of the vector space

## Homogeneous system

Given 3 linear equations equal to 0, then the matrix formed by the equations is homogeneous.

The left part is called the coefficient matrix.

## Rank

If of m equations in a system, k can be expressed as a linear combination of the other m - k equations, then we really only have m - k equations to work with (the others can be reduced to 0=0). This value is called the rank of the system, denoted r.

- If r < n, then the system is under-determined (infinite amount of solutions -> solutions are expressed as linear combinations)
- If r = n, then there is only one solution to the system. 
- If r > n, then the system is over-determined (thus inconsistent since solutions are contradictory)

## Determinant

Determinant of order 2 (2 by 2 matrix) : det(A) = |A| = a11a22 - a12a21 (diagonals)

Determinant of higher order is defined recursively : 
- D = SUM(aijCij) for j=1 to n  (which is equal to the sum over rows instead of columns)
- C being the co-factor Cij = (-1)^(i+j) * Mij
- M being the minor of aij which is the Determinant of the submatrix corresponding to aij
- The submatrix corresponding to aij is the matrix where the ith row and the jth column have been deleted
- Determinant do not change for the transposed matrix and also do not change not matter which row or column is chosen in the SUM
- If a matrix has a zero column or row, its determinant is zero
- Multiplying every element in a row or a column of a matrix by the constant c results in multiplying its determinant by the same factor.
- Interchanging two rows or columns of matrix A results in a matrix B such that detB = -detA. 
- If a matrix has identical rows or columns, its determinant must be zero, because zero is the only number whose negation leaves it unchanged.
- A square matrix with n rows and columns has rank n if and only it has a non-zero determinant.
- A square matrix has an inverse (is non-singular) if and only if has a non-zero determinant.

## Cramer's Theorem/rule

If a system of n linear equations in n variables Ax = b has a non-zero coefficient determinant D = det A then the system has only one solution, given by xi = Di/D (Di = determinant of a matrix obtained by substituting b for the ith column in A)

If b = 0, the system is homogeneous -> Di = 0 -> xi = 0

If D = 0, variables are assigned indeterminate quantity 0/0.

## Inverse of a matrix

A * A^-1 = A^-1 * A = I

A^-1 = (1/|A|) * [Cjk]^T  (Cjk being the co-factor of ajk)

If A is not invertible, it's a singular matrix. det(Singular Matrix) = 0

(when order 2, A^-1 is easier : 1/|A| * [(a22 -a12)(-a21 a11)])

## Eigenvalue/vector

- When the result of a matrix multiplication with a particular vector is the same as a scalar multiplication with that vector, we call the scalar an eigenvalue of the matrix and the corresponding vector an eigenvector.
- Thus, an Eigenvalue of a Square Matrix A is a scalar LAMBDA such that, for some non-zero column eigenvector x,  Ax = LAMBDA x
- The magnitude of an eigenvalue indicates the degree to which the matrix operation scales an eigenvector: the larger the magnitude, the greater the scaling effect.
- We can find the Eigenvalues by resolving the roots of the characteristic polynomial, resulting of the characteristic equation given by the characteristic determinant equal to zero : |A - LAMBDA * I| = 0
- Eigenvalues of the transposed matrix are the same
- The set of eigenvalues of a matrix is called its spectrum.
- The largest eigenvalue by magnitude is called the principal eigenvalue or the spectral radius of the matrix.
- Principal egenvalues are important to approximate the limit of n applications of a matrix to a vector.
- Principal/Dominant egenvalue can be estimated using the power method which applies A and computes the Rayleigh ratio repeatedly
- We can also estimate the dominant eigenvector with the power method (but instead of computing the Rayleigh ratio, we have to rescale the vector such that the largest element is 1)
- The set of eigenvectors corresponding to a set of distinct eigenvalues are always linearly independent of each other.
- The set of all vectors that can be expressed as a linear combination of the eigenvectors is called the eigenspace of the matrix.
- The elements of a Diagonal matrix ARE the Eigenvalues
- If a matrix is square and symmetric (that it, A^T = A), then its eigenvalues are real.
- Gerschgorin’s ‘circle’ theorem : if the off-diagonal elements are ‘not too large,’ then the eigenvalues of the matrix are its diagonal elements
- The eigenvectors corresponding to a set of distinct eigenvalues form a linearly independent set. Hence, if a square matrix of order n has n distinct eigenvalues, we can express any initial vector as a linear combination of its eigenvectors.

