# pyATS & Genie

## Good to know

- The devices keys MUST mirror the actual hostnames in `testbed.yaml`. If it doesn't, `pyats` gets stuck on device prompt (with no error or indication)

## Quick usage

- Validating a testbed file : `pyats validate testbed testbed.yaml`

- Python shell with auto imports : `pyats shell --testbed-file testbed.yaml`

- A device can be retrieved by its alias : 
```python
>>> local = testbed.devices['local']
>>> local.connect()
>>> output = local.parse("show interface")
```

- Equivalent of the above but on bash directly : `pyats parse "show ip interface brief" --testbed-file ./testbed.yaml`

- Getting all infos from all devices in the testbed : 
`pyats learn all --testbed-file testbed.yaml --output learn-all-20200416 -qqq`

- Doing a diff between 2 directories of infos learnt : 
`pyats diff learn-all-20200416 learn-all-20200416-2 --no-default-exclusion --exclude "age" "uptime" --output diffs -qqq`

- Launching a predefined full test case (harness) :
`pyats run genie --testbed-file testbed.yaml ----trigger-uids="TriggerClearIpRoute" --verification-uids="Verify_IpRoute_vrf_all" --devices remote`

- Checking the logs of the previous test run nicely formatted in the browser : 
`pyats logs view`

- Using 'API' predefined functions (not much available on `nxos` though)
`local.api.get_running_config_dict()`

- Quick Non-Agnostic configuration : 
```python
device.configure('''
  interface Ethernet1/1
  no shutdown
''')
```


