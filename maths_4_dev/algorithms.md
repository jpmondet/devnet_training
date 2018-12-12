# Al-Khwarizmi

- Mathematical abstraction of computer program
- Computational procedure to solve a problem
- Goes with a Model of Computation 

## Model of Computation 

Specifies what operations an algorithm is allowed to use, the cost of each
operation and the cost of the algorithm.

## Time Complexity

Python Operations : https://wiki.python.org/moin/TimeComplexity  (regex not
shown but re. is in general exponential time !!)

## Insertion Sort

```
for j <- 2 to n
 insert key A[j] into the (already sorted) sub-array A[1 .. j-1].
  by pairwise key-swaps down to its right position
```

THETA(n^2) compares & THETA(n^2) swaps

## Binary Insertion Sort

```
for j <- 2 to n
 insert key A[j] into the (already sorted) sub-array A[1 .. j-1].
 Use binary search to find the right position
```
Binary search : THETA(log n)
Shifting elements after insertion : THETA(n)
  -> THETA(n.log n)
Swaps : THETA(n^2)

## Merge Sort

Divide & conquer concept

```
If n = 1, done (nothing to sort).
Otherwise, recursively sort A[ 1 . . n/2 ] and A[ n/2+1 . . n ] .
“Merge” the two sorted sub-arrays.
```

Recursively sorting 2 subarrays : 2T(n/2)
Merge : THETA(n)
  -> THETA(n.log n)


