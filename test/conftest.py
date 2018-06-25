import pytest
import requests
from authnid.make_app import make_app, make_config
from .helpers import relative_dir
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
                relative_dir("ssl/client-certs/atat.mil.crt"),
                relative_dir("ssl/client-certs/atat.mil.key"),
            ),
        ):
            return self.client.get(self.server_api, cert=certs, allow_redirects=False)

    return RequestClient(server_api)


@pytest.fixture
def app():
    config = make_config()
    app = make_app(config)
    app.user_repo.autocommit = False
    return app


@pytest.fixture
def client(app):
    return app.test_client()
