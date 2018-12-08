# Theorems/rules/formulas

## The Well Ordering Principle

Every nonempty set of nonnegative integers has a smallest element.

## The Induction Principle 

### Ordinary Induction

Let P be a predicate on nonnegative integers. If

- P(0) is true
- And P(n) IMPLIES P(n+1) for all nonnegative integers, n
- Then P(m) is true for all nonnegative integers, m.

### Strong Induction

Let P be a predicate on nonnegative integers. If

- P(0) is true
- And for all nonnegative integers n, P(0), P(1), ..., P(n) TOGETHER imply  P(n+1) 
- Then P(m) is true for all nonnegative integers, m.

## The Principle of Structural Induction

Let P be a predicate on a recursively defined data type R. If

- P(b) is true for each base case element, b in R
- And for all two-argument constructors, c, [P(r) AND P(s)] IMPLIES P(c(r,s)) for all r, s in R,
and likewise for all constructors taking other numbers of arguments,
- Then P(r) is true for all r in R.

## Zermelo-Fraenkel Set Theory with Choice (ZFC)

### Extensionality

Two sets are equal if they have the same members.

### Pairing

For any two sets x and y, there is a set, {x, y}, with x and y as its only elements

### Union

The union, u, of a collection, z, of sets is also a set

### Infinity

There is an infinite set. Specifically, there is a nonempty set, x, such that for any set y in x, the set {y} is also a member of x.

### Subset

Given any set, x, and any definable property of sets, there is a set containing precisely those elements y in x that have the property

## Power Set

All the subsets of a set form another set.

### Replacement

The image of a set under any definable function will also fall inside a set. 

### Foundation

There cannot be an infinite sequence of sets each of which is a member of the previous one.

(or every nonempty set has a “member-minimal” element.)

### Choice

Given a set, s, whose members are nonempty sets no two of which have any element in common, then there is a set, c, consisting of exactly one element from each set in s.

## The Invariant Principle

If a preserved invariant of a state machine is true for the start state, then it is true for all reachable states.

## General Principle of Remainder Arithmetic

To find the remainder on division by n of the result of a series of additions and multiplications, applied to some integers

- replace each integer operand by its remainder on division by n,
- keep each result of an addition or multiplication in the range [0..n) by immediately replacing any result outside that range by its remainder on division by n.


## Modus Ponens

This rule says that a proof of P together with a proof that
P IMPLIES Q is a proof of Q. (P, P IMPLIES Q / Q)  _(the slash "/" should be an
horizontal bar)_

## Quadratic formula 

If ax^2 + bx + c = 0 and a != 0, then x = (-b +/- SQRT(b^2 - 4ac)) / 2a

## Goldbach's Conjecture

If n is an even integer greater than 2, then n is a sum of two primes.

## Standard deviation

Square root of the Variance (which is the average of the squared differences
from the Mean.)

The standard deviation (sigma) of a sequence of values x1, ..., xn is zero
iff all the values are equal to the mean.

## Summation

1+2+3+...+n = n(n+1)/2 for all nonnegative integers, n.

## Fundamental theorem of arithmetic

Every positive integer greater than one can be factored as a product of primes.

## Implication

An implication is true exactly when the if-part is false or the then-part is true.

(that is, it is only false when the if-part is true AND the then-part is false)

## If and only If (iff)

The proposition “P if and only if Q” asserts that P and Q have the same truth value. Either both are true or both are false.

## Proposition in normal form

Every propositional formula is equivalent to both a disjunctive normal form and a conjunctive normal form.

## DeMorgan's Laws

NOT(A AND B) <-> NOT(A) OR NOT(B)

NOT(A OR B) <-> NOT(A) AND NOT(B)

## Derived variables

1. If f is a strictly decreasing N-valued derived variable of a state
machine, then the length of any execution starting at state q is at most f(q)

2. If there exists a strictly decreasing derived variable whose range
is a well ordered set, then every execution terminates.

## Schroder-Bernstein

For any sets A, B, if A surj B and B surj A, then A bij B

(holds on infinite sets)

## Cantor

For any set, A, A strict pow(A)   

(even for inifinite sets!)

## Division Theorem

Let n and d be integers such that d > 0.
Then there exists a unique pair of integers q and r, such that

n = q * d + r AND 0 <= r < d

(Even with n < 0, the remainder is positive!!)

## Euclid's Algorithm

Recursively based on gcd(a,b) = gcd(b, rem(a,b))  for b != 0

## The Pulverizer

The greatest common divisor of a and b is a linear combination of a and b. That is,

gcd(a,b) = sa + tb  for some integers s & t

An integer is a linear combination of a and b iff it is a multiple of gcd(a, b).

(Basicaly, The Pulverizer Algorithm takes the same steps as Euclid's but
keeping the combination r = x - qy of each steps to find the latest reminder's
combination that is not 0)

## Prime Number Theorem 

lim (x -> inf) (Pi(n) / (n/ln n)) = 1

(Pi(n) being the number of primes up to n)

## Chebyshev's Theorem on Prime Density

For n > 1, Pi(n) > (n / 3ln n)

## Fundamental Theorem of Arithmetic (Unique Factorization Theorem)

Every positive integer is a product of a unique weakly decreasing sequence of primes.

### Lemmas

- If p is a prime and p divides ab, then p divides a or p divides b
- Let p be a prime. If p divides a1a2...an, then p divides some ai

## Relative Primality

If k in [0..n) is relatively prime to n, then k has an inverse in Zn.

If i and j are both inverses of k in Zn, then i = j (unique inverse)

## Cancellation

A number k is cancellable in Zn iff ka = kb implies a = b (Zn) for all a,b in [0..n)

If k has an inverse in Zn, then it is cancellable.

## Euler's Function

For n > 0, PHI(n) ::= the number of integers in [0..n) that are relatively prime to n

PHI(pq) = (p-1)(q-1) for primes p != q

If p is a prime, then PHI(p^k) = p^k - p^(k-1) for k >= 1

If a and b are relatively prime, then PHI(ab) = PHI(a)PHI(b)

## Euler's Theorem

If n and k are relatively prime, then k^(PHI(n)) is congruent to 1 (mod n)

For all k in Zn(star), k^(PHI(n)) = 1 (Zn)

### Fermat's Little Theorem

Suppose p is a prime and k is not a multiple of p, then: k^(p-1) is congruent to 1 (mod p)

## Graph theory

The shortest walk from one vertex to another is a path.

The shortest positive length closed walk through a vertex is a cycle through that vertex.

### The Triangle Inequality

dist(u,v) <= dist(u,x) + dist(x,v) for all vertices u, v, x with equality holding iff x is on a shortest path from u to v

### Adjacency Matrices

If C is the length-k walk counting matrix for a graph G, and D is the length-m walk counting matrix, then CD is the length k + m walk counting matrix for G.

The length-k counting matrix of a digraph, G, is (Ag)^k for all k in N

### DAGs

Every finite DAG has a topological sort.

In a DAG, D, if the size of the largest chain is t , then V(D) can be partitioned into t antichains.

**Dilworth's Lemma** : For all t > 0, every DAG with n vertices must have either a chain of size greater than t or an antichain of size at least n/t.

Every DAG with n vertices has a chain of size greater than sqrt(n) or an antichain of size at least sqrt(n).

For any digraph, G, the walk relations G+ and G* are transitive

For any digraph, G, the walk relation G* is reflexive

R is a DAG iff R+ is irreflective.

A relation R is a strict partial order (transitive & irreflexive) iff R is the
positive walk relation of a DAG.

A digraph D is a DAG iff D+ is asymmetric.

A relation is a weak partial order iff it is the walk relation a of DAG. (same
as strict but antisymettric, that is the condition is relaxed when a vertex is
compared to itself)

Every weak partial order is isomorphic to the subset relation on a collection
of sets.

Every strict partial order is isomorphic to the proper subset relation on a collection
of sets.

### Simple Graphs

**Handshaking Lemma** : The sum of the degrees of the vertices in a simple graph equals twice the number of edges.

A graph, G, with at least one edge is bipartite iff its chromatic number = 2

A graph with maximum degree at most k is (k+1)-colorable.

The following graph properties are equivalent : 
- The graph contains an odd length cycle.
- The graph is not 2-colorable.
- The graph contains an odd length closed walk.

If two vertices are k-connected, then there are k edge-disjoint paths connecting them.

Every graph, G, has, at least, |V(G)| - |E(G)| connected components

Every connected graph with n vertices has at least n-1 edges.

### Trees

Every tree has the following properties : 
- Every connected subgraph is a tree.
- There is a unique path between every pair of vertices.
- Adding an edge between nonadjacent nodes in a tree creates a graph with a cycle.
- Removing any edge disconnects the graph. That is, every edge is a cut edge.
- If the tree has at least two vertices, then it has at least two leaves.
- The number of vertices in a tree is one larger than the number of edges.

Every connected graph contains a subgraph that is a tree with the same vertices as the graph. This is called a **spanning tree**.

An edge extends a pre-MST F if it is a minimum weight gray edge in some solid coloring of F.

If all edges in a weighted graph have distrinct weights, then the graph has
a unique MST.

#### Algorithms to find MST

[Prim] Grow a tree one edge at a time by adding a minimum weight edge among the edges that have exactly one endpoint in the tree.

[Kruskal] Grow a forest one edge at a time by adding a minimum weight edge among the edges with endpoints in different connected components.

Grow a forest one edge at a time by picking any component and adding a minimum weight edge among the edges leaving that component.

## Geometric series

If |x| < 1, then SUM(x^i) from i=0 to inf  is equal to  1 / (1-x)

If |x| < 1, then SUM(ix^i) from i=0 to inf  is equal to  x / (1-x)^2

## Approximation of Sums

Let f:R+ -> R+ be a weakly inscreasing function. Define S :== SUM(f(i)) from
i=0 to n ;  and I :: { f(x)dx  from 1 to n   ( { being the integral)

Then I + f(1) <= S <= I + f(n)

Similarly, if f is weakly descreasing, then I + f(n) <= S <= I + f(1)

## Products

Any product can be converted into sum by taking a logarithm.

## Asymptotic notation

x^a = o(x^b) for all nonnegative constants a < b

x^b = o(a^x) for any a,b in R with a > 1

If f = o(g) or f ~ g, then f = O(g)

f = Theta(g) iff f = O(g) and g = O(f)

## Counting sets

**binomial coefficient** (n choose k) = n! / (k!(n-k)!)

**multinomial coefficient** (n choose k1,k2,...km) ::= n! / (k1!k2!...km!)

**Binomial Theorem** : (a+b)^n = SUM( (n choose k) * a^(n-k) * b^k) from k = 0 to n 

**Multinomial Theorem** : (z1 + z2 + ... + zm)^n = SUM( (n choose k1, k2,...km) * z1^k1 * z2^k2...zm^km) for k1,...km in N such as k1 + ...+ km = n

## Pigeonhole Principle

If |A| > |B|, then for every total function f:A->B, there exist two different
elements of A that are mapped by f to the same element of B.

**Generalized** :  If |A| > k.|B|, then for every total function f:A->B maps at least k+1 different elements of A to the same element of B.

## Probabily rules for Sets

**Sum Rule** : If E0,E1, ... En, ...  are **pairwise disjoint events** then
Pr[UNION(En) for n in N] = SUM(Pr[En]) for n in N

**Union Bound** : Pr[E1 U ... U En U ...] <= Pr[E1] + ... + Pr[En] + ...

Let X and Y be events where Y has nonzero probability, then Pr[X|Y] :;= Pr[X
INTERSECTION Y] / Pr[Y]

Pr[E1 INTERSECTION E2] = Pr[E1] . Pr[E2 | E1]

Pr[E1 INTERSECTION E2 INTERSECTION E3] = Pr[E1] . Pr[E2 | E1] . Pr[E3 | E1
INTERSECTION E2]

**Bayes' Rule** : P[B|A] = Pr[A|B].Pr[B] / Pr[A]

**Law of Total Probabily** : Pr[A] = Pr[A|E].Pr[E] + Pr[A|notE].Pr[notE]
