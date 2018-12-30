# Signals, Systems and Transforms

**Signal** : Series of numbers/vectors or continuous function of time with different characteristics (discrete/continuous, digital/analog, periodic/aperiodic, time-limited/unlimited, time-shifted, time-scaled)

**System** : Process that converts input signals to output signals

**Transform** : Changes the Basis of a signal. In Computer Networking,
the basis of sinusoids are what we care about.

**Sinusoid** : Carrier signal associated with a time period T such that, at time t, the amplitude of the signal is defined by **cos(2.PI.t/T)**

What is interesting about Sinusoid is that it can by modelized by a vector (phasor) on a disk of radius 1 that rotates at constant angular velocity w (little omega) with a period of T seconds.

w = 2.PI / T -> THETA = 2.PI.t/T = wt  (THETA being the phase angle made by the phasor and the x axis in radians (2PI radians = 360degrees))

![circle](./random_web_findings/circle-calculus.jpg)

## Complex numbers

- i can be seen as the 90-degree rotation operator of a vector. 
- j^2 = -1 (the vector (0,0)(0,1) rotated 2 times) ->  j = SQRT(-1)
- Thus, we can draw a plane with reals as x axis and imaginaries as y axis. 
- Any vector on this plane can be represented as the vector sum a + ib (or a + jb)
- z = a+ib is a complex number; a = Re(z); b = Im(z); zSTAR = a-ib (z * is the complex conjugate)

## Euler's formula

The phasor is "conveniently" represented by **ce^(iTHETA) = c(cos(THETA) + isin(THETA))** (c being the magnitude of the vector)

a + ib = c.cos(THETA) + c.i.sin(THETA) => a = c.cos(THETA) ; b = c.sin(THETA)
; c = SQRT(a^2 + b^2) ; THETA = arctan(b/a)

Also cos(THETA) = 1/2 (e^(iTHETA) + e^(-iTHETA)) and sin(THETA) = 1/2i (e^(iTHETA) - e^(-iTHETA))

![Pythagorean](./random_web_findings/pythagorean.jpg)

## Convolution (that is really convoluted...)

DELTA (or Impulse) function is used to "select" part of a function (for continuous functions, delta is the special DIRAC-DELTA) by being 1 where we want to select and 0 otherwise 

## Discrete functions

x(t) (×) y(t) = SUM(x(TO)y(t-TO)) for TO = -INF to +INF

(the symbol (×) replace the real symbol * since it is now wrongly seen as a simple multiplication)

## Continuous functions

x(t) (×) y(t) = INTEGRAL(x(TO)y(t-TO))dTO for TO = -INF to +INF

## The complex exponential signal

ke^(st) where s = ALPHA + iOMEGA 

Expanding it gives : ke^(ALPHA.t) * cos(OMEGA.t) + ike^(ALPHA.t) * sin(OMEGA.t)

This signal is interesting because it can represents a variety of signals, for example : 
- s=0 -> we get the constant signal k
- OMEGA=0 -> real monotone exponentiel signal ke^(ALPHA.t)
- s = +/- iOMEGA -> sinusoids
- ALPHA = 0 -> helix (whose projections are sinusoids)
- Finally, exponentially modulated helix (whose projections are exponentially modulated sinusoids)

![exp-signals-1](./random_web_findings/exp-signals-1.png)

![exp-signals-2](./random_web_findings/exp-signals-2.png)


