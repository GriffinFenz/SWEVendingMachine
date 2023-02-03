from dataclasses import dataclass

import pytest
from flask.testing import FlaskClient

from app import create_app
from app.models.testdb import run_db


@pytest.fixture()
def app():
    app = create_app()
    run_db(app)

    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@dataclass
class Tester:
    __test__ = False
    test_client: FlaskClient

    @staticmethod
    def expect(response, code):
        return response.json.get("STATUS_CODE") == code
