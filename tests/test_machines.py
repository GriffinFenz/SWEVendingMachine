import pytest

from app.extensions import db
from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    return MachineTester(test_client=client)


class MachineTester(Tester):
    def get_machine(self, machine_id):
        return self.test_client.get("/machine", query_string={"id": machine_id})


def test_get_machine(tester):
    get_response = tester.get_machine("1")
    assert Tester.expect(get_response, 200)

    machine = get_response.json.get("Machine")

    assert machine is not None

    assert machine.get("machine_name") == "Bob"
    assert machine.get("machine_location") == "here"
