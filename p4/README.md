# P4-16 Learnings

Some notes on the course materials released by [Eth Zurich](https://adv-net.ethz.ch/) on their [github](https://github.com/nsg-ethz/p4-learning).

## Intro slides

- Presents the usual "SDN" & OpenFlow concepts
- The drawbacks of Openflow
- PISA (Protocol Independent Switch Architecture) composition
  - Parser
    - Parse packet headers and metadata using a state machine
    - 3 predefined states (start, accept, reject) (p.109)
  - Ingress match-action pipeline
    - control flow
      - apply changes to packets
    - actions
      - code reuse (functions)
    - tables
      - match key in a table (like fib)
      - return possible/default actions doable on the table with this key
  - Switching logic (crossbar/buffers,..)
  - Egress match-action pipeline
  - Deparser
    - Reassemble the modified packets
- P4 (domain-specific language) describes how a PISA should process packets

## Day 2

- p4-14 initiated in 2014 and stabilized in 2015
- p4-16 spec in 2017
- The latter is the focus of this course
- p4 Architecture (provided by the vendor): 
  - simply an API to program a target 
  - there are multiple architectures for different targets
  - defines the metadata it supports
  - defines "extern" interfaces (closed-source functions)
- p4-16 language :
  - statically-typed
  - base types + structs ("header" which contains a hidden "validity" field)
  - headers can be stacked
  - headers (exclusive) union
  - some basic C-like operations (but not division, nor modulo..)
  - also C-like variables/constants
    - variables have local scope ! No state maintained between packets ! (tables or externs can be used for this)
  - basic statements (return, exit, if/else, switch)
  - https://p4.org/p4-spec/docs/P4-16-v1.0.0-spec.html


  


