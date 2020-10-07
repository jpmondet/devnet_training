from scrapli.driver.core import NXOSDriver, AsyncNXOSDriver
from asyncio import get_event_loop

n9kv_ssh = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 8181,
    "auth_username": "admin",
    "auth_password": "Admin_1234!",
    "auth_strict_key": False,
    "transport": "asyncssh",
}


async def get_running():
    async with AsyncNXOSDriver(**n9kv_ssh) as nx:
        result = await nx.send_command("sh run")
    print(result.result)


def main():
    async_scrapli = True
    if not async_scrapli:
        conn = NXOSDriver(**n9kv_ssh)
        conn.open()
        response = conn.send_command("show run")
        print(response.result)
    else:
        get_event_loop().run_until_complete(get_running())


if __name__ == "__main__":
    main()
