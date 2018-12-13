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

## Breadth-First Search

(with SPF at the same time)

Graph represented as adjacency list

```
bfs(s.Adj):
 level = { s: 0}
 parent = { s: None }
 i = 1
 frontier = [s]
 while frontier:
  next = []
  for u in frontier:
   for v in Adj[u]:
    if v not in level:
     level[v] = i
     parent[v] = u
      next.append(v)
  frontier = next
  i++
```

SUM(|Adj[v]|) for v in V  = 2.|E|

## Depth-First Search

```
parent = { s: None }
dfs-visit(V, Adj, s):
 for v in Adj[s]:
  if v not in parent:
   parent[v]= s
   DFS-Visit(V,Adj,v)

dfs(V, Adj):
 parent = {}
 for s in V:
  if s not in parent:
   parent[s] = None
    dfs-visit(V, Adj, s)
```

THETA(V+E)
