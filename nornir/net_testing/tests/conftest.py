import pytest

from nornir import InitNornir


@pytest.fixture(scope="session", autouse=True)
def nr():
    nr = InitNornir(
        core={"num_workers": 5},
        inventory={
            "plugin": "nornir.plugins.inventory.ansible.AnsibleInventory",
            "options": {
                "hostsfile": "hosts"
            }
        }
    )
#   Using the config_file as parameter is not working for whatever reason
#    return InitNornir(config_file="config.yaml")
    return nr
