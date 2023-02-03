import pytest
from typing import Dict

from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    return MachineTester(test_client=client)


class MachineTester(Tester):
    def get_machine(self, machine_id):
        return self.test_client.get("/machine", query_string={"id": machine_id})

    def get_all_machines(self):
        return self.test_client.get("/all-machines")

    def create_machine(self, json: Dict[str, str]):
        return self.test_client.post("/machine/create", json=json)

    def delete_machine(self, json: Dict[str, int or str]):
        return self.test_client.delete("/machine/delete", json=json)

    def edit_machine(self, json: Dict[str, str]):
        return self.test_client.put("/machine/edit", json=json)


def test_get_machine(tester):
    get_response = tester.get_machine("1")
    assert Tester.expect(get_response, 200)

    machine = get_response.json.get("Machine")

    assert machine is not None

    assert machine.get("machine_name") == "Bob"
    assert machine.get("machine_location") == "here"


def test_get_all_machines(tester):
    get_response = tester.get_all_machines()
    assert Tester.expect(get_response, 200)

    machine_1 = get_response.json.get("Machine")[0]
    machine_2 = get_response.json.get("Machine")[1]

    assert machine_1 is not None
    assert machine_2 is not None

    assert machine_2.get("machine_name") == "BetterBob"
    assert machine_2.get("machine_location") == "there"


def test_create_machine_success(tester):
    json = {"machine_name": "Bob2", "location": "no"}
    get_response = tester.create_machine(json)
    assert Tester.expect(get_response, 200)

    machine = get_response.json.get("Machine")

    assert machine is not None

    assert machine.get("machine_name") == "Bob2"
    assert machine.get("machine_location") == "no"


def test_create_machine_fail_key_error(tester):
    json = {"a": "a", "location": "a"}
    get_response = tester.create_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing location or/and machine_name parameters"


def test_create_machine_fail_exists(tester):
    json = {"machine_name": "Bob", "location": "a"}
    get_response = tester.create_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Machine already exists"


def test_delete_machine_success(tester):
    json = {"machine_id": 2}
    get_response = tester.delete_machine(json)
    assert Tester.expect(get_response, 200)

    message = get_response.json.get("message")

    assert message == "Machine with id: '2' has been deleted"


def test_delete_machine_fail_key_error(tester):
    json = {"a": 2}
    get_response = tester.delete_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing machine_id parameter"


def test_delete_machine_fail_not_found(tester):
    json = {"machine_id": 60}
    get_response = tester.delete_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "No machines that matches the id: '60'"


def test_edit_machine_success(tester):
    json = {"machine_id": 2, "machine_name": "NewBob", "location": "same place"}
    get_response = tester.edit_machine(json)
    assert Tester.expect(get_response, 200)

    machine = get_response.json.get("Machine")

    assert machine is not None

    assert machine.get("machine_name") == "NewBob"
    assert machine.get("machine_location") == "same place"


def test_edit_machine_fail_key_error(tester):
    json = {"machine_id": 1, "a": "a", "b": "b"}
    get_response = tester.edit_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing machine_id/location/machine_name parameter"


def test_edit_machine_fail_duplicate(tester):
    json = {"machine_id": 2, "machine_name": "Bob", "location": "no"}
    get_response = tester.edit_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Machine with name: 'Bob' already belongs in the database"


def test_edit_machine_fail_not_found(tester):
    json = {"machine_id": 60, "machine_name": "hi", "location": "no"}
    get_response = tester.edit_machine(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Machine with id: '60' does not exist"
