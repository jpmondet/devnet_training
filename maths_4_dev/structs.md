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

For any node x, for all nodes y in the left subtree of x, key(y) <= key(x).
Right subtree -> key(y) >= key(x)

Operations in O(height):  (height should be O(log n) but worst case can become
O(n) if tree not balanced at all)
- Insert value
- Find value
- Find min/max value (go always left or right)

Easily augmented (nodes can store more data)
