import pytest
from typing import Dict
from werkzeug.test import TestResponse

from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    return StockTester(test_client=client)


class StockTester(Tester):
    def stock_add(self, json: Dict[str, str or int]):
        return self.test_client.post("/stock/add", json=json)

    def stock_edit(self, json: Dict[str, str or int]):
        return self.test_client.put("/stock/edit", json=json)


def test_stock_add_success(tester):
    json = {"product_id": "2", "machine_id": "2", "amount": 5}
    get_response = tester.stock_add(json)
    assert Tester.expect(get_response, 200)

    machine_stock = get_response.json.get("MachineStock")

    assert machine_stock is not None

    assert machine_stock.get("stock_quantity") == 5


def test_stock_add_key_error(tester):
    json = {"a": "a"}
    get_response = tester.stock_add(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing product_id/machine_id parameter"


def test_stock_add_value_error(tester):
    json = {"machine_id": 1, "product_id": 1, "amount": "a"}
    get_response = tester.stock_add(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Amount entered is not a valid number"


def test_stock_add_already_exists(tester):
    json = {"machine_id": 1, "product_id": 1, "amount": 100}
    get_response = tester.stock_add(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "The Product with id: 1 already exists in Machine with id: 1"


def test_stock_edit_success(tester):
    json = {"product_id": "1", "machine_id": "1", "amount": 10}
    get_response = tester.stock_edit(json)
    assert Tester.expect(get_response, 200)

    machine_stock = get_response.json.get("MachineStock")

    assert machine_stock is not None

    assert machine_stock.get("stock_quantity") == 10


def test_stock_edit_key_error(tester):
    json = {"a": "a"}
    get_response = tester.stock_edit(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing product_id/machine_id parameter"


def test_stock_edit_value_error(tester):
    json = {"machine_id": 1, "product_id": 1, "amount": "a"}
    get_response = tester.stock_edit(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Amount entered is not a valid number"


def test_stock_edit_does_not_exist(tester):
    json = {"machine_id": 2, "product_id": 2, "amount": 10}
    get_response = tester.stock_edit(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "The stock does not not currently exists"
