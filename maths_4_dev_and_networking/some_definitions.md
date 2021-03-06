# Definitions

- N => set of nonegative integers
- Z => set of integers
- Q => set of rational numbers
- R => set of real numbers
- C => set of complex numbers

A **proposition** is a statement (communication) that is either true or false.

A **predicate** can be understood as a proposition whose truth depends on the value of one or more variables.

Important true propositions are called **theorems**.

A **lemma** is a preliminary proposition useful for proving later propositions.

A **corollary** is a proposition that follows in just a few logical steps from a theorem.

**Axioms** are simply accepted propositions.

**Logical deductions**, or **inference rules**, are used to prove new propositions using previously proved ones. (example: _Modus Ponens_)

A **proof** is a sequence of logical deductions from axioms and previously proved statements that concludes with the proposition in 
question.

A number is **rational** when it equals a quotient of integers

A **valid** formula is one which is always true, no matter what truth values its variables may have.

A **satisfiable** formula is one which can sometimes be true—that is, there is some assignment of truth values to its variables that makes it true.

A statement P is satisfiable iff its negation NOT(P) is not valid.

A **disjunctive form** is simply an OR of AND -terms, where each AND -term is an AND of variables or negations of variables, for example, (A AND B) OR (A AND C)

A **disjunctive normal** form (DNF) is a disjunctive form where each AND -term is an AND of every one of the variables or their negations in turn.

A **conjunctive form** is an AND of OR -terms in which the OR -terms are OR ’s only of variables or their negations.

A **conjunctive normal form** (CNF) is a conjunctive form where earch OR-term is an OR of every one of the variables or their negations in turn.

**P** stands for problems whose instances can be solved in time that grows polynomially with the size of the instance.

**NP** stands for nondeterministtic polynomial time.

The **Power Set** pow(A) is the set of all the subsets of a set A. If A has
n elements, then there are 2^n sets in pow(A)

A **binary relation**, R, consists of a set, A, called the domain of R, a set, B,
called the codomain of R, and a subset of AxB called the graph of R (can be
visualized as "Archery"). More specifically, a binary relation, R, is :

- a function when it has the [<= 1 arrow out] property.
- surjective when it has the [>= 1 arrows in] property. That is, every point in
the righthand, codomain column has at least one arrow pointing to it.
- injective when it has the [>= 1 arrows out] property.
- bijective when it has both the [= 1 arrow out] and the [=1 arrow in]
  property.
- total when it has the [>= 1 arrows out] property. 

The **Image** of a set, Y, under a relation, R, written R(Y), is the set of
elements of the codomain, B, of R that are related to some element in Y. 
In terms of the relation diagram, R(Y is the set of points with an arrow coming
that starts from some point in Y.

If A is a finite set, the **cardinality** of A, written |A|, is the number of elements in A.

 - If A surj B, then |A| >= |B|
 - If A inj B, then |A| =< |B|
 - If A bij B, then |A| = |B|
 - |A| = n -> |pow(A)| = 2^n
 - A strict B iff NOT(A surj B)
 - A strict B iff |A| < |B|
 - A surj B iff B inj A
 - If A surj B and B surj C, then A surj C
 - If A bij B and B bij C, then A bij C
 - A bij B iff B bij A

An **execution** of the state machine is a (possibly infinite) sequence of states with the property that

 - it begins with the start state,
 - and if q and r are consecutive states in the sequence
 - then q -> r

A **preserved invariant** of a state machine is a predicate, P , on states, such that 
 - whenever P(q) is true of a state, q, 
 - and q -> r for some state, r,
 - then P(r) holds.

A **derived variable** f : states -> R is stricly decreasing iff q -> q'
IMPLIES f(q') < f(q)

It is weakly decreasing iff q -> q' IMPLIES f(q') <= f(q)

Definitions of **recursive data types** have two parts:

- Base case(s) specifying that some known mathematical elements are in the
data type 
- and Constructor case(s) that specify how to construct new data elements from
previously constructed elements or from base elements.

**Structural Induction** is a method for proving that all the elements of a recursively
defined data type have some property.

A set is **countable** iff it is finite or countably infinite. 

A set, C, is **countable** iff N surj C. In fact, a nonempty set C is
countable iff there is a total surjective function g : N -> C

A set, C, is **countably infinite** iff N bij C. (exples : Z+, Z, NxN, N, Q+,
ZxZ, Q)

a is **congruent** to b modulo n iff n divides (a-b) (iff rem(a,n) = rem(b, n))

The **ring of integers modulo n** Zn is the set of integers in the range [0..n) together with the operations (+n) and (.n).   (+n being the addition followed by the remainder)

Integers that have no prime factor in common are called **relatively prime** (gcd(a,b) = 1))

A **directed graph** (digraph), G, consists of a nonempty set, V(G), called the vertices of G, and a set, E(G), called the (directed) **edges** (or arrows) of G. An element of V(G) is called a **vertex** (or node).

A **directed edge** starts at some vertex, u, called the **tail** of the edge and ends at some vertex, v, called the **head** of the edge.

The **in-degree** of a vertex in a digraph is the number of arrows coming into it, and similarly its **out-degree** is the number of arrows out of it.

A **walk** in a digraph, G, is an alternating sequence of vertices and edges that begins with a vertex, ends with a vertex, and such that for every edge (u -> v) in the walk, vertex u is the element just before the edge, and vertex v is the next element after the edge

A **closed walk** is a walk that begins and ends at the same vertex.

A **cycle** is a positive length closed walk whose vertices are distinct except for the beginning and end vertices

The walk is a **path** iff all the vertices are different.

A **merge f^r**, is a walk that starts with a walk f and continue with a walk r (merge of 2 walks)

The vertex e where the walks merge can be specified in the notation: **fêr**.

The **distance**, dist(u, v), in a graph from vertex u to vertex v is the length of a shortest path from u to v

An **adjacency matrix** is a representation of a Graph as an nxn matrix of
zeroes and ones. (n being the vertices v0,v1, ..., v(n-1)). The ijth entry
of the adjacency matrix is 1 if there is an edge from vertex vi to vertex vj
and 0 otherwise

The length-k **walk counting matrix** for an n-vertex graph G is the nxn matrix
C such that Cuv ::= the number of length-k walks from u to v.

The **walk relation** on V(G) is the binary relation G* where u G* v :== there is a walk in G from u to v.

When there is a walk from vertex v to vertex w, we say that w is **reachable** from v, or equivalently, that v is **connected** to w.

Let R: B -> C and S: A -> B be binary relations. Then the **Composition of Relations** R with S is the binary relation (R o S): A -> C 

A **directed acyclic graph** (DAG) is a directed graph with no cycles.

A **topological sort** of a finite DAG is a list of all the vertices such that
each vertex v appears earlier in the list than every other vertex reachable
from v.

A vertex v of DAG, D, is **minimum** iff every other vertex is reachable from
v.

A vertex v is **minimal** iff v is not reachable from any other vertex.

Two vertices in a DAG are **comparable** when one of them is reachable from the other.

A **chain** in a DAG is a set of vertices such that any two of them are comparable.

A largest **chain** ending at an element a is known as a **critical path**. The number of elements less than a in the chain is 
called the **depth** of a.

A vertex in a chain that is reachable from all other vertices in the chain is called a **maximum element** of the chain.

A finite chain is said to **end at** its maximum element.

A **schedule** for performing tasks specifies which tasks to do at successive steps.

A **partition** of a set A is a set of nonempty subsets of A called the **blocks** of the partition, 
such that every element of A is in exactly one block.

A **parallel schedule** for a DAG, D is a partition of V(D) into blocks 
Ao, A1, ..., such that when j < k, no vertex in Aj is reachable from any vertex
in Ak. The block Ak is called the set of elements **scheduled at step k**, and
the **time of the schedule** is the number of blocks. The maximum number of
elements scheduled at any step is called the **number of processors** required
by the schedule.

A **minimum time schedule** for a finite DAG D consists of the sets A0, A1, ..., where Ak ::= {a in V(D) | depth(a) = k}

**Parallel time** = **size** of a critical path.

An **antichain** in a DAG is a set of vertices such that no two elements in the set are comparable. That is no walk exists between any two different vertices in the set.

A binary relation, R, on a set, A, is **isomorphic** to a relation, S, on a set
B iff there is a relation-preserving bijection from A to B; that is, there is
a bijection f : A -> B such that, for all a, a´ in A : a R a´ iff f(a) S f(a´)

A partial order for which every two different elements are comparable is called
a **linear order**.

A relation is an **equivalence** relation if it is reflexive, symmetric and
transitive.

Given an equivalence relation R : A -> A, the **equivalence class** of an
element a in A is the set of all elements of A related to a by R.

The equivalence classes of an equivalence relation on a set A are the blocks of a partition of A.

**Simple graphs** are defined as digraphs in which edges are undirected.

Two vertices in a simple graph are said to be **adjacent** iff they are the endpoints of the same edge, and an edge is said to be **incident** to each of its endpoints.

**Complete graph** == full mesh

The **Empty graph** has no edges at all.

The **Line graph** is an n-node graph containing n-1 edges in sequence.

Adding the edge (vn_v1) to the Line Graph result in a **length-n Cycle Graph**

An **Isomorphism** between 2 graphs is an edge-preserving bijection between
their sets of vertices. The 2 graphs are said **Isomorphic**.

A **bipartite** graph is a graph whose vertices can be partitioned into two
sets, L(G) and R(G), such that every edge has one endpint in L(G) and the
endpoint in R(G).

A Graph is **k-colorable** if it has a coloring that uses at most k colors.

The minimum value of k for which a graph, G, has a valid coloring is called its
**chromatic number**. 

A graph is **connected** when every pair of vertices are connected.

A **connected component** of a graph is a subgraph consisting of some vertex and every node and edge that is connected to that vertex.

Two vertices in a graph are **k-edge connected** when they remain connected in every subgraph obtained by deleting up to k 1 edges.

A graph is **k-edge connected** when it has more than one vertex, and pair of distinct vertices in the graph are k-connected.

If two vertices are connected in a graph G, but not connected when an edge e is removed, then e is called a **cut edge** of G.

An acyclic graph is called a **forest**. A connected acyclic graph is called
a **tree**.

A degree 1 node in a forest is called a **leaf**.

The **weight of a graph** is the sum of the weights of its edges.

A **minimum weight spanning tree** (MST) of an edge-weighted graph G is
a spanning tree of G with the smallest possible sum of edge weights.

A **pre-MST** for a graph G is a spanning subgraph of G that is also a subgraph of some MST of G.

If F is a pre-MST and e is a new edge, that is e in E(G)-E(F), then
e **extends** F when F+e is also a pre-MST.

Let F be a pre-MST, and color the vertices in each connected component of F either all black or all white. At least one component of each color is required. Call this a **solid coloring** of F. A **gray edge** of a solid coloring is an edge of G with different colored endpoints.

**Geometric series** is a sum where the ratio between successive terms is fixed.

The nth **harmonic number**, Hn, is Hn :== SUM(1/i) from i=1 to n

For functions f,g:R->R, f is **asymptotically equal** to g (f(x) ~ g(x)) iff
lim(x->inf) f(x)/g(x) = 1

For f,g:R->R, with g nonnegative, f is **asymptotically smaller** than g, f(x) = o(g(x)) iff lim(x->inf) f(x) / g(x) = 0

For f,g:R->R, with g nonnegative, f = O(g) iff limSup(x->inf) |f(x)| / g(x) < INF

(n over k) red **n choose k** ::= the number of k-element subsets of an n-element set

**(n choose k)** = n! / (k!(n-k)!)

A countable **sample space** S is a nonempty countable set. An element w in
S is called an **outcome**. A subset of S is called an **event**.

A **probability function** on a sample spaceS is a total function Pr:S->R
such that : Pr[w] >= 0 for all w in S  and SUM(Pr[w]) = 1 for w in S

A sample space together with a progrability function is called a **probability
space**. 

For any event E, the **probability** of E is defined to be the sum of the
probabilities of the outcomes in E : Pr[E] ::= SUM(Pr[w]) for w in E

A finite probability space S is said to be **uniform** if Pr[w] is the same for
every outcome w in S.  Any even E in S : Pr[E] = |E| / |S|

The expressions Pr[X|Y] denotes the probability of event X, **given that** event
Y happens.

Event A is **independent** of event B iff Pr[A|B] = Pr[A] or said differently : Pr[A INTERSECTION B] = Pr[A].Pr[B] /!\ DISJOINT EVENTS ARE NEVER INDEPENDENT

A set of events A1, A2, ... , is **k-way independent** iff every set of k of
these events is mutually independent. The set is **pairwise independent** iff
it is 2-way independent.

A **random variable** R on a probability space is a total function whose domain
is the sample space.

An **indicator random variable** (also called **Bernouilli variables**) is a random variable that maps every outcome
to ether 0 or 1.

The **probability density function** (PDF(R(x))) of a random variable R, measures the
probability that R takes the value x.

The **cumulative distribution function**, (CDF(R(x))) measures the probability
that R <= x.

A **Bernouill distribution** is the distribution function for a Bernouilli variable.

A random variable that takes on each possible value in its codomain with the
same probability is said to be **uniform**.

The **expectation** of a random variable R is its average value when each value
is weighted according to its probability. If R is defined on a sample space S,
then the expectation of R is :  Ex[R] ::=  SUM(R(w)Pr[w]) for w in S

Given a random variable R, the expected value of R **conditioned on a event A**
is the probability-weighted average value of R over outcomes in A : Ex[R|A] :==
SUM(r.Pr[R=r|A]) for r in range(R)

A random variable C has a **geometric distribution** with parameter p iff
codomain(C) = Z+ and Pr[C=i] = p.(1-p)^(i-1)

The **Linearity of Expectation** means that the expected value of a sum of
random variables is the sum of the expected values of the variables Ex[a1R1+a2R2] = Ex[a1R1] + Ex[a2R2]  (can be generalized with SUM())

The **variance** (also known as **mean square deviation**) Var[R] of a random variable R is : Var[R] ::= Ex[(R-Ex[R])^2]

The **standard deviation** SIGMA(R) of a random variable R is the square root
of the variance.

An assignment of probabilities to vertices in a digraph is a **stationary
distribution** if for all vertices x Pr[at x] = Pr[go to x at next step]

Strongly connected graphs have **unique** stationary distributions.
