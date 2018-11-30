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
