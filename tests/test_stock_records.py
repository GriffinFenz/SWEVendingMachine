import pytest
from werkzeug.test import TestResponse
import time

from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    client.post("/stock/add", json={"product_id": "2", "machine_id": "2", "amount": 2})
    # risky so might need to fix
    client.put("/stock/edit", json={"product_id": "2", "machine_id": "2", "amount": 5})
    time.sleep(2)  # For testing purposes
    client.put("/stock/edit", json={"product_id": "2", "machine_id": "2", "amount": 30})
    return StockRecordTester(test_client=client)


class StockRecordTester(Tester):
    def get_product_time_stamp_in_records(self, product_id):
        return self.test_client.get(
            "/product/records", query_string={"product_id": product_id}
        )

    def get_machine_time_stamp_in_records(self, machine_id):
        return self.test_client.get(
            "/machine/records", query_string={"machine_id": machine_id}
        )


def test_product_time_stamp_success(tester) -> TestResponse:
    get_response = tester.get_product_time_stamp_in_records("2")
    assert Tester.expect(get_response, 200)

    records = get_response.json.get("Records")

    first_quantity = records[0].get("stock_quantity")
    second_quantity = records[1].get("stock_quantity")

    assert records is not None

    assert first_quantity == 5
    assert second_quantity == 30


def test_product_time_stamp_fail(tester) -> TestResponse:
    get_response = tester.get_product_time_stamp_in_records("30")
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Stock with product id: '30' not found"


def test_machine_time_stamp_success(tester) -> TestResponse:
    get_response = tester.get_machine_time_stamp_in_records("2")
    assert Tester.expect(get_response, 200)

    records = get_response.json.get("Records")

    first_quantity = records[0].get("stock_quantity")
    second_quantity = records[1].get("stock_quantity")

    assert records is not None

    assert first_quantity == 5
    assert second_quantity == 30


def test_machine_time_stamp_fail(tester) -> TestResponse:
    get_response = tester.get_machine_time_stamp_in_records("30")
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Stock with machine id: '30' not found"
