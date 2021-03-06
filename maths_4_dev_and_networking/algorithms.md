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

### Pseudopolynomial

The problem is polynomial in size (cardinality) BUT is also polynomial in the Numbers size of the input (for example, pseudopolynomial behave differently where, with the same number of entries, each entry is a very large number)

## Computational complexity

- P = problems solvable in polynomial (n^c) time
- NP = decision problems with solutions that can be “checked” in polynomial time (the algo being nondeterministric (lucky guessing))
- NP-Complete = Hardest problems in NP
- NP-hard = as hard as every problem in NP
- EXP = problems solvable in exponential (2^n^c) time
- (same concepts for EXP-Complete/hard)
- R = problems solvable in finite time
- P C EXP C R

## High precision arithmetic

In python, following algorithms are implemented in [gmpy2](https://pypi.org/project/gmpy2/) package

### Multiplication

- Karatsuba (THETA(d^lg3))
- Toom-Cook (THETA(d^1.465))
- Schönhage-Strassen (THETA(d.lg d.lg ld d))
- Furer (THETA(n.log n.2^O(log * n)))   (log "star" being iterated log)

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

O(V+E)

## Depth-First Search

```
dfs_visit(V, Adj, s):
 for v in Adj[s]:
  if v not in parent:
   parent[v]= s
   dfs_visit(V,Adj,v)

dfs(V, Adj):
 parent = {}
 for s in V:
  if s not in parent:
   parent[s] = None
    dfs_visit(V, Adj, s)
```

THETA(V+E)

## Topological Sort

Reverse of DFS. In fact the algorithm of DFS can be reused and just add an
array to get the order :  

```
dfs_visit(V, Adj, s):
 ...
 order.append(v)

dfs(V, Adj):
 ...
 order.reverse()
```

(This is true because the visit of a children is ended before the visit of a parent)


## Counting Sort

Generally better than comparison based sorts when elements are in range from
1 to k.

```
counting_sort(A):
 L = [[] for i in range(len(A))] 
 for j in range n:
  L[key(A[j])].append(A[j])
 output = []
 for i in range len(L):
  output.extend(L[i])
```

THETA(n+k) (time & space)

## Radix Sort

When elements are in range from 1 to n^2, Counting Sort could become worse than
comparison based algos.

To get over this problem, Radix Sort splits into subproblems (digit level) and
applies Counting Sort (or other Stable Sort) to the subproblems.

```
radix_sort(A):
 for i in A.length - 1:
  stable_sort(s[i]])
```

THETA(d * (n+b)) (d=digits & b=base) 

-> Can be minimized with b=n & k <= n^constant -> becomes O(nc)

## Dijkstra 

```
relax(u,v,w,Q):
 if Q[v] > Q[u] + w(u,v):
  Q[v] = Q[u] + w[u,v] 

dijkstra(V,s,w)
 S = {}
 Q = V // V contains graph vertexes
 initialize(Q) //(every distance to vertex of Q to INF except source)
 while len(Q) != 0:
  u, S[u] = extract-min(Q)  //Q is a Priority Queue. Extract withdraw u from Q
  for v in Adj(u):
   relax(u,v,w,Q)  //(updates distances of Q if needed)
```

THETA(V.log V + E) (with Priority Queue beeing a Fibonacci heap)

### Optimizations 

- If shortest path is needed only for 1 source and 1 target, stop after
  extracting the target from the Priority Queue

- Bi-Directional Search : Worst case may not be better but can be faster in
  other cases.

- Goal-Directied Search (A "star") : Basically modify weights to be able to
  apply Dijkstra.

## Bellman-Ford

Particularity : Won't die if there is negative cycles.
However, the complexity is higher than Dijkstra.

```
bf(G,s,w):
 S = {}
 Q = G.V
 initialize(Q)  //every dist(v) to INF except the source 
 for _ in range(len(Q)):
  for edge(u,v) in G.E:
   relax(u,v,w,Q)
 for edge(u,v) in G.E:  // This part only check for cycles
  if Q[v] > Q[u] + w[u,v]:
   ABORT() // There is a negative, the algo must stop and shortest path is undefined
```

O(VE) (but E can be O(V^2))

## Dynamic Programming

- Invented by Bellman 
- ~ guessing + (recursion + memoization) or Bottom-up (same computation but without recursion so faster in practice and can save space)
- time = number of subproblems * time per subproblem

### Steps

- Define subproblems
- Guess (guess which other subproblems to use)
- relate subproblems solutions
- recurse + memoize / bottom-up   (must check that subproblems are acyclic
  / in topological order)
- solve original problem based on subproblems

Subproblems for multiple strings/sequences -> combine suffix/prefix/substring subproblems
