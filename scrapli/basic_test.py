from scrapli.driver.core import NXOSDriver

n9kv_ssh = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 8181,
    "auth_username": "admin",
    "auth_password": "Admin_1234!",
    "auth_strict_key": False,
}

conn = NXOSDriver(**n9kv_ssh)
conn.open()
response = conn.send_command("show run")
print(response.result)
