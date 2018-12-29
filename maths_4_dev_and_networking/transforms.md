# Signals, Systems and Transforms

**Signal** : Series of numbers/vectors or continuous function of time  

**System** : Process that converts input signals to output signals

**Transform** : Changes the Basis of a signal. In Computer Networking,
the basis of sinusoids are what we care about.

**Sinusoid** : Carrier signal associated with a time period T such that, at time t, the amplitude of the signal is defined by **cos(2.PI.t/T)**

What is interesting about Sinusoid is that it can by modelized by a vector (phasor) on a disk of radius 1 that rotates at constant angular velocity w (little omega) with a period of T seconds.

w = 2.PI / T -> THETA = 2.PI.t/T = wt  (THETA being the phase angle made by the phasor and the x axis in radians (2PI radians = 360degrees))

## Complex numbers

- i can be seen as the 90-degree rotation operator of a vector. 
- j^2 = -1 (the vector (0,0)(0,1) rotated 2 times) ->  j = SQRT(-1)
- Thus, we can draw a plane with reals as x axis and imaginaries as y axis. 
- Any vector on this plane can be represented as the vector sum a + ib (or a + jb)
- z = a+ib is a complex number; a = Re(z); b = Im(z); zSTAR = a-ib (z * is the complex conjugate)
