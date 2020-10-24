# Automapping [Work in Progress]

(will eventually be in its own repo at some point in time)

The goal here is to have an automated replacement to weathermap.  
That means that this project aims to output a map of the network topology and regularly poll the devices to show the links utilization.

This is an ambitious goal but we'll see how far we can go...


## Some ideas to start with

- Get devices/links datas by leveraging LLDP recursively starting from 
- Build a graph (networkx) from those datas
- Generating an html/js output to show the graph on a browser

At this point, we have the net topology drawn.  
However, still nothing about link utilization.

- Scrap devices interfaces utilization (snmp or ssh? ssh seems overkill for this. Telemetry is so badly supported by net vendors that it's not really a solution)
- Store those datas on a DB (need at least a 3 months of storage)
- Depending on time frame chosen, average the values and colorize the links accordingly

Or 

- Leverage datas already store in cacti..

