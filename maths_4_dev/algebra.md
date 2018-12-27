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


