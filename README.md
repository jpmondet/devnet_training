# devnet_training
Some network-oriented developments using APIs/Netconf/Yang/etc. (self-trainings, nothing fancy)

# Some reminders/cheatsheets

## Yang

``pyang --tree-help``

``pyang -f tree <yang_module>``

``pyang -f tree --tree-path path/to/target <yang_module>``

``pyang -f tree --tree-depth 2 <yang_module>``

**Getting Netconf ready formats :** (the output might need some corrections though)
``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target <yang_module>``

``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target --sample-xml-skeleton-doctype=config  <yang_module>``


**Validating modules :**
``pyang --lint <yang_module>``

**Generating python :**
``export PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print("%s/plugin" % os.path.dirname(pyangbind.__file__))'```
``pyang -p /path/to/target --plugindir $PYBINDPLUGIN -f pybind openconfig-bgp.yang > openconfig-bgp.py``

