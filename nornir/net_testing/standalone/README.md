# Network tests with nornir

(This is not to be used in production. It's just a lil' example for my future self)

## Usage

Variables to be tested can be at multiple places:
- Hosts
- Host_vars
- Group_vars
- to_validate.yaml (only this one is used for now but inventory vars could be more interesting to use for production to be more flexible)

`pytest --verbose .`

For now, it tests only configured vlan & configured bgp as & neighbors.

TODO: 
- Add "state" tests.
- Find ways to be less vendors dependant (unfortunately yang is still useless for this right now since support is still very poor)
