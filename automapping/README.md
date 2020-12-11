# Automapping [Work in Progress]

(will eventually be in its own repo at some point in time)

The goal here is to have an automated replacement to weathermap.  
That means that this project aims to output a map of the network topology and regularly poll the devices to show the links utilization.

This is an ambitious goal but we'll see how far we can go...


## Some ideas to start with

- Get devices/links datas by leveraging LLDP recursively starting from 1 or 2 devices (recursively because we can have some unknown devices on large snow flakes topologies)
- Build a graph (networkx) from those datas
- Generate an html/js output to show the graph on a browser with plotly

At this point, we have the net topology drawn.  
However, still nothing about link utilization.  
Plotly doesn't allow to display a table or something when hovering links (except by hiding transparent nodes on links... Not very satisfying.) and  
colorization depending on link utilization isn't doable either.

For next steps (particularly the third one), I'll have to reshape my lost forgotten frontend skills : 

- Scrap devices interfaces utilization (snmp or ssh? ssh seems overkill for this. Telemetry is so badly supported by net vendors that it's not really a solution right now :-\ )
  - would be interesting to look at pushing solutions instead of pulling from devices
- Store those datas on a DB (need at least 3 months storage)
- Depending on time frame chosen, average the values and colorize the links accordingly

Or 

- Leverage datas already stored in something like cacti as weathermap did... (but clearly not an ideal solution since cacti doesn't have a proper API)
