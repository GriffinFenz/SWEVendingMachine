import pytest
from werkzeug.test import TestResponse

from tests.conftest import Tester


@pytest.fixture()
def tester(client):
    return AppTester(test_client=client)


class AppTester(Tester):
    def index(self):
        return self.test_client.get("/")


def test_app_success(tester) -> TestResponse:
    get_response = tester.index()
    assert Tester.expect(get_response, 200)
    assert get_response.json.get("success")
