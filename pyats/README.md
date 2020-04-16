# pyATS & Genie

## Bugs to know

- The devices keys MUST mirror the actual hostnames in `testbed.yaml`. If it doesn't, `pyats` gets stuck on device prompt (with no error or indication)

## Quick usage

`pyats validate testbed testbed.yaml`

`pyats shell --testbed-file testbed.yaml`

```
>>> local = testbed.devices['local']
>>> local.connect()
>>> output = local.parse("show interface")
```


