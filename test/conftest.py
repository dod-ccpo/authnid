import requests
import pytest
import os


@pytest.fixture(scope='module')
def server_api():
    host = os.getenv('SERVER_NAME')
    server_name = f'https://{host}'
    return server_name
