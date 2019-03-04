# P4-16 Learnings

Some notes on the course materials released by [Eth Zurich](https://adv-net.ethz.ch/) on their [github](https://github.com/nsg-ethz/p4-learning).

## Intro slides

- Presents the usual "SDN" & OpenFlow concepts
- The drawbacks of Openflow
- PISA (Protocol Independent Switch Architecture) composition
  - Parser
  - Ingress match-action pipeline
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
  - some basic C-like operations (also bitwise like `<<` but not division, nor modulo..)
  - also C-like variables/constants
    - variables have local scope ! No state maintained between packets ! (tables or externs can be used for this)
  - basic statements (return, exit, if/else, switch)
  - https://p4.org/p4-spec/docs/P4-16-v1.0.0-spec.html

### Parser
- Parse packet headers and metadata using a state machine
- 3 predefined states (`start`, `accept`, `reject`) (p.109)
- optional `transition` statement to transfer to another state
  - can `select` states depending on header fields
```
state parse_ethernet {
  packet.extract(hdr.ethernet);
  transition select(hdr.ethernet.etherType) {
    0x800: parse_ipv4;
    default: accept;
  }
}
```
- support fixed & variable-length (`varbit`) header extraction
- parser can loop on header stack (this is the only looping ability in p4) by letting a state `select` itself
- advanced concepts to check :
  - `verify` : error handling in the parser
  - `lookahead` : access bits that are not parsed yet
  - `sub-parsers` ~~ subroutines

### Control 

#### Tables
- Kind of definition of a table
 - How and what keys are matched
 - Which actions are doable
 - Size
 - Default action
- Can match 1 or multiple keys
- key are `field: match type`. Match types are defined in P4 core library and architectures (p.68)

#### Actions
- Blocks of statements that possibly modify packets
- Code reuse (functions)
- "Directional" parameters (`in`, `out`, `inout`)
- If parameter comes from a table lookup (control-plane), can't be directional

#### Control flow
- Interact with tables (applies, checks)
 - Apply changes to packets by using actions
 - Can do checks such as :
  - `if` there was a hit
  - `switch` between actions to know which one was executed
  - checksums
- clone packets
- send packets to control-plane
- recirculate packets

## Day 3

### State(ful|less) programming in p4 with basic structures

- Statesless objects
 - Variables
 - Headers
- Stateful objects
 - Tables (cp)
 - Registers 
 - Counters
 - Meters
 - ...

#### Registers

Allows storing arbitrary value.

Assigned in arrays

`register<bit<48>>(16384) name_of_register;`

Interact using `.read()`, `.write()`

### Counters

Different types of counters
 - packets
 - bytes
 - packets_and_bytes

Assigned in arrays

`counter(512,CounterType.packets) pkt_counter;`

Can just `.count()`. Reading is done by control-plane only (ex p.35).

There are also **direct counters** that can be attached to a table (in the definition) (ex p.37)

#### Meters

Some kind of policer/rate-limiter.

Assigned in arrays.

`meter(32w16384, MeterType.packets) pkt_meter;`

The meter can :
- executed `.execute_meter<bit<32>>(meter_index, meta.meter_tag);`
- red `.read(meta.meter_tag);`

A table's key can also handle packets depending on the meter tag.

The concept of **direct** meter also applies here.

### Advanced structures

#### Implementing a Set

1. As separate chaining
2. As a simple hashmap
3. Bloom filters (multi-hash)

#### Implementing a set with Bloom Filter (as a set)

Sizing can be found with `K = ln 2 * (M/N)` where
- K = number of hash functions
- M = cells
- N = elements
with a False Positive rate of ~ `(1-e^(-KN/M))^K`

The `v1model` contains the needed HashAlgorithms & a hash function (ex p.94)

There are drawbacks tho : 
- Hardware limitations (could require to split the bloom filter)
- Reset the bloom filters instead of deletion (either choose an alternative to bloom filter or 2 bloom filters to avoid the resetting time)
 - Example of alternative (p.109): **Counting Bloom Filters** (p.109) or **ILBT** (p.) 
 - [more about Bloom Filters](https://en.wikipedia.org/wiki/Bloom_filter)

## Day 4

In depth into data structures and more specifically **Sketches** to be able to get how frequently a flow appears.

## Day 5

Example of applications : 

- NetChain : Interesting In-network key-value store leveraging programmable hardware with p4.
- NetCache : Load-balancing for a key-value store using small & very fast cache of the switch asics.

In both cases, custom UDP-based protocols are used.

## Last day

Some more examples of applications seen in researches : 

- CONGA : Improving ECMP-like load-balancing in DC tracking congestion to minimize bottlenecks (+ diminushing issues during link failures)
  - See also : HULA (INT + routing), DRILL, LetFlow..
- INT : In-band Network Telemetry  
- p4v : P4 programs verification (proof/correctness)
- Swing State : Management of programmable networks

## Debugging options (learned from exercises)

Adding `--log-console` to `cli_input` in the `p4app.json` enable logging to a file each packet processing which can be extremely insightful.

The switch_cli (`simple_switch_CLI --thrift-port 9090`) provides infos on tables and other usefull stuff with, for example, `table_dump MyIngress.macAddrTable`.
