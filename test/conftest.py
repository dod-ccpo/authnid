import pytest
from authnid.make_app import make_app
import os


@pytest.fixture(scope='module')
def server_api():
    host = os.getenv('SERVER_NAME')
    server_name = f'https://{host}'
    return server_name

@pytest.fixture
def app():
    return make_app({})

@pytest.fixture
def client(app):
    return app.test_client()

