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

## Counting Sort

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
