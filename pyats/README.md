# pyATS & Genie

__Looks like it doesn't work very well for nxos.. Stuck on prompt__

## Quick usage

`pyats shell --testbed-file testbed.yaml`

```
>>> local = testbed.devices['local']
>>> local.connect()
>>> output = local.parse("show interface")
```
