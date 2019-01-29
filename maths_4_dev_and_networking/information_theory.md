# Information theory

## Mathematical model for Communication

Assuming a system with only 1 source, 1 receiver and 1 channel, a model can
define the state of knowledge of a receiver. When the receiver receive
a message over the channel, its knowledge increases by the **information content** of the message.

The model implies being able measure the receiver's knowledge. 

In a situation where the source have to send 1 of N equiprobable messages, if
the receiver knows it will receive 1 of N message but doesn't know which one,
we call the **entropy** (H) the initial degree of uncertainty of the receiver : H = log N (the log base 2 comes from the fact that it can be modelized as a binary tree)

However, if the messages are not equiprobable, the entropy becomes dependent of the probabilities of each message.

This can be modelized by defining a random variable (X) corresponding to a chosen message and having discrete values x1, x2, ... xN such that P{X=xi} = P(xi) and then taking the entropy of this random variable : H(X) = -SUMi(P(xi).log P(xi))

Note that entropies of independent random variables are additive : H(XY) = H(X) + H(Y)


/!\ This is assuming that messages to be sent are finite and we know the probability to select one message or the other. This limitation is addressed by :
 - representing the infinite set of messages as **symbols**
 - computing entropy at the symbol level (**symbol entropy**)
 - identifying the underlying alphabet of symbols and computing the relative frequencies of occurrence of longer and longer symbol sequences in a representative message corpus we can approximately determine its entropy.


To shorten the messages as much as possible, the symbols are encoded. But from this, arise the problem of finding the **optimal encoding**. 

A code should be **unambiguous** to avoid confusing the receiver. Also it should (but nowadays, it is not really mandatory/true) be an **instantaneous code** (code that can be decoded immediately -> no codeword should be the prefix of another one).

But to be optimal, instantaneous is not enough, the code must also : 
- construct message symbols from longer sequences of elementary symbols (which makes it more efficient)
- take probabilities into account by assigning shorter codes to frequent symbols

**Kraft inequality** : SUMi(2^(-li)) <= 1  (for instantenous code and with li being the level in the binary tree of the code).  It constrains the choice of codeword lengths

It permits to show that the expected length of a codeword is lower-bounded by entropy : E >= H(X)

The **Huffman code** approaches H. It even guarantees to have an average
codeword no longer than H+1. It is found by assigning symbols to leaf nodes of a tree sorted by probabilities of those symbols (least-likely to most-likely).

