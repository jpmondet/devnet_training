## Priority Queue

A data structure implementing a set S of elements, each associated with a key, supporting the following operations:
- insert(S, x) : insert element x into set S
- max(S) : return element of S with largest key
- extract_max(S) : return element of S with largest key and remove it from S
- increase_key(S, x, k) : increase the value of element x’ s key to new value k (assumed to be as large as current value)

## Heap

- Impl of Priority Queue
- Array visualized as binary tree of height O(lg n)
  - root : first elem of array
  - parent(i) = i/2
  - left(i) = 2i
  - right(i) = 2i+1
- Operations :
  - build_max_heap : from unordered array, order such that the key of a node is >= keys of its children (O(n))
```
build_max_heap(A):
 for i=n/2 down to 1:
  max_heapify(A, i)
```
  - max_heapify(i) : if max heap is changed, allow re-sorting the subtree rooted at index i (in O(log n))
```
(A = the heap)

max_heapify(A, i)
l = left(i)
r = right(i)
if (l <= heap-size(A) and A[l] > A[i])
then
 largest = l 
else
 largest = i
if (r <= heap-size(A) and A[r] > A[largest])
then largest = r
if largest != i
then exchange A[i] and A[largest]
 max_heapify(A, largest)
```
  - insert
  - extract_max
  - heapsort (O(nlog n))
    - build_max_heap()
    - recursively 
      - swap A[n] and A[1] to get max at the end of the array
      - Discard node n
      - max_heapify if the swap broke max_heap

## Binary Search Trees (BST)

Rooted binary tree 

Each node has typically:
- a key
- a left pointer
- a right pointer
- a parent pointer

For any node x, for all nodes y in the left subtree of x, key(y) <= key(x).
Right subtree -> key(y) >= key(x)


Operations in O(height):  (height should be log n but worst case can become n if tree not balanced at all)
- Insert value
- Find value
- Find min/max value (go always left or right)

Easily augmented (nodes can store more data)

## Balanced BST

Balanced BST came to life because of the worst case of BST (h = n). It aims to
keep the height to log n.

### AVL (Adel'son-Vel'skii & Landis) Trees

For every node, require heights of left & right children to differ by at most +/- 1 ("nil" subtree has a height of -1)

Augments nodes by storing they height

Use of rotating to correct violation of the AVL rule.

Must be done at each insert/delete.

### Many more Balanced BST, including as research topics

## Dictionaries

- Pre-hashing (keys must be nonnegative integers)
- Hashing
  - Division Method : h(k) = k mod m  (m = nb of slots in the table)
  - Multiplication method: h(k) = [(ak) mod 2^w] >> (w-r)     (a random, w is the nb of bits of k)
  - Universal Hashing: h(k) = [(ak+b) mod p] mod m   (p = large prime)
- Start with small table and grow when needed (usually mx2 and shrink by 2 when m/4)
  - Needs rehashing when growing/shrinking the table
- Collisions
  - Chaining (linked list in each slots)
  - Open addressing (multiple trials to success having all items in slots of the table)
    - Linear Probing (but can create clusters of items)
    - Double Hashing (degrades heavily when the slot are above 70% utilized)

## Graph Representations

### Adjacency lists

For each vertex u in V, Adj[u] stores u's neighbors (only outgoing edges if directed)

(Adj can be a list or a dict)

### Implicit Graphs

Adj(u) is a function

### Object oriented

### Neighbor lists

Vertices are objects and u.neighbors is a list (for example)

### Incidence Lists

Vertices are objects and u.edges is a list of (outgoing) edges.





