#! /usr/bin/env python3

import asyncio

from scrapli.driver.core import NXOSDriver, AsyncNXOSDriver
from ttp import ttp


n9kv_ssh = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 8181,
    "auth_username": "admin",
    "auth_password": "Admin_1234!",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "platform": "nxos",
}

switches = [ n9kv_ssh ]

drivers = { 'nxos': AsyncNXOSDriver }

cmds = { 'nxos': 'sh run' }

async def agnosticonfig(switch):

    driver = drivers[switch['platform']]
    cmd = cmds[switch['platform']]

    # scrapli doesn't expect 'platform' keyword
    switch.pop('platform') 

    async with driver(**switch) as sw:
        result = await sw.send_command(cmd)

    return result.result
    



async def get_config():
    coroutines = [ agnosticonfig(switch) for switch in switches ] 

    results = await asyncio.gather(*coroutines)

    with open('ttp.tplate', 'r') as tplate:
        tplate_text = tplate.read()
        for result in results:
            parser = ttp(result, tplate_text)
            parser.parse()
            print(parser.result())


def main():
    async_scrapli = True
    if not async_scrapli:
        conn = NXOSDriver(**n9kv_ssh)
        conn.open()
        response = conn.send_command("show run")
        print(response.result)
    else:
        asyncio.get_event_loop().run_until_complete(get_config())


if __name__ == "__main__":
    main()
