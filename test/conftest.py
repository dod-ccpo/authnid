import pytest
import requests
from authnid.make_app import make_app, make_config
from authnid.make_db import connect_db, make_cursor
from authnid.user_repo import UserRepo
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
    return make_app(config)


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_repo(database):
    return UserRepo(database, autocommit=False)

@pytest.fixture(scope="module")
def database():
    db_uri = make_config()['DATABASE_URI']
    return make_cursor(connect_db(db_uri))

@pytest.fixture(scope='function')
def reset(database):
    yield
    database.execute("TRUNCATE users;")
    database.connection.commit()
