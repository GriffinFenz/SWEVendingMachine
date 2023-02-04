import pytest
from typing import Dict
from werkzeug.test import TestResponse

from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    return ProductTester(test_client=client)


class ProductTester(Tester):
    def get_product(self, product_id):
        return self.test_client.get("/product", query_string={"id": product_id})

    def get_all_products(self):
        return self.test_client.get("/all-products")

    def create_product(self, json: Dict[str, str or int]):
        return self.test_client.post("/product/create", json=json)

    def delete_product(self, json: Dict[str, str or int]):
        return self.test_client.delete("/product/delete", json=json)

    def edit_product(self, json: Dict[str, str or int]):
        return self.test_client.put("/product/edit", json=json)


def test_get_product(tester) -> TestResponse:
    get_response = tester.get_product("1")
    assert Tester.expect(get_response, 200)

    product = get_response.json.get("Product")

    assert product is not None

    assert product.get("product_name") == "Coke"
    assert product.get("product_price") == "20.00"


def test_get_all_products(tester) -> TestResponse:
    get_response = tester.get_all_products()
    assert Tester.expect(get_response, 200)

    product_1 = get_response.json.get("Product")[0]
    product_2 = get_response.json.get("Product")[1]

    assert product_1 is not None
    assert product_2 is not None

    assert product_2.get("product_name") == "Cookies"
    assert product_2.get("product_price") == "100.00"


def test_create_product_success(tester) -> TestResponse:
    json = {"product_name": "Sprite", "price": 10}
    get_response = tester.create_product(json)
    assert Tester.expect(get_response, 200)

    product = get_response.json.get("Product")

    assert product is not None

    assert product.get("product_name") == "Sprite"
    assert product.get("product_price") == "10.00"


def test_create_product_key_error(tester) -> TestResponse:
    json = {"a": "a", "b": "b"}
    get_response = tester.create_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing price or/and product_name parameters"


def test_create_product_value_error(tester) -> TestResponse:
    json = {"product_name": "Sprite", "price": "apple"}
    get_response = tester.create_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Price entered is not a valid number"


def test_create_product_already_exists(tester) -> TestResponse:
    json = {"product_name": "Coke", "price": 100}
    get_response = tester.create_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Product already exists"


def test_delete_product_success(tester) -> TestResponse:
    json = {"product_id": "1"}
    get_response = tester.delete_product(json)
    assert Tester.expect(get_response, 200)

    message = get_response.json.get("message")

    assert message == "Product with id: '1' has been deleted"


def test_delete_product_key_error(tester) -> TestResponse:
    json = {"a": "a"}
    get_response = tester.delete_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing product_id parameter"


def test_delete_product_wrong_id(tester) -> TestResponse:
    json = {"product_id": 10}
    get_response = tester.delete_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "No products that matches the id: '10'"


def test_edit_product_success(tester) -> TestResponse:
    json = {"product_id": 1, "product_name": "New Coke", "price": 5}
    get_response = tester.edit_product(json)
    assert Tester.expect(get_response, 200)

    product = get_response.json.get("Product")

    assert product is not None

    assert product.get("product_name") == "New Coke"
    assert product.get("product_price") == "5.00"


def test_edit_product_key_error(tester) -> TestResponse:
    json = {"a": "a", "b": "b", "c": "c"}
    get_response = tester.edit_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Missing product_id/price/product_name parameter"


def test_edit_product_value_error(tester) -> TestResponse:
    json = {"product_id": 1, "product_name": 3, "price": "c"}
    get_response = tester.edit_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Price entered is not a valid number"


def test_edit_product_already_exists(tester) -> TestResponse:
    json = {"product_id": 2, "product_name": "Coke", "price": 10}
    get_response = tester.edit_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Product with name: 'Coke' already belongs in the database"


def test_edit_product_id_mismatch(tester) -> TestResponse:
    json = {"product_id": 10, "product_name": "a", "price": 10}
    get_response = tester.edit_product(json)
    assert Tester.expect(get_response, 400)

    message = get_response.json.get("message")

    assert message == "Product with id: '10' does not exist"
