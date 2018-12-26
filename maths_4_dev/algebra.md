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

## Field

A field is a (in)finite set that supports the operations of addition and
multiplication on elements of this set. Also satifies : 
- Closure (for a, b in F, if a+b=c and a * b = d, then c,d are also in F)
- Commutativity
- Associativity
- Identity (0 for addition & 1 for multiplication)
- Inverses
- Distributivity
