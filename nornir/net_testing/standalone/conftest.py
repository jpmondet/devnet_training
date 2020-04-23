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
    return nr
