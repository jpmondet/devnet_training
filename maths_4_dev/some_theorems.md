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


