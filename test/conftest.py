import pytest
import requests
from authnid.make_app import make_app
import os


@pytest.fixture
def server_api():
    host = os.getenv("SERVER_NAME")
    server_name = f"https://{host}"
    return server_name


@pytest.fixture
def request_client(server_api):

    class RequestClient():

        def __init__(self, server_api):
            self.client = requests.Session()
            self.server_api = server_api

        def login(
            self,
            certs=(
                "/app/ssl/client-certs/atat.mil.crt",
                "/app/ssl/client-certs/atat.mil.key",
            ),
        ):
            return self.client.get(self.server_api, cert=certs, allow_redirects=False)

    return RequestClient(server_api)


@pytest.fixture
def app():
    return make_app({})


@pytest.fixture
def client(app):
    return app.test_client()
