import os
import re
import pytest
import requests
import urllib3
from test.helpers import is_token, relative_dir
from authnid.make_app import make_config
from authnid.user_repo import UserRepo

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
            # we do not care about the host cert here
            self.client.verify = False
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.server_api = server_api

        def login(
            self,
            certs=(
                relative_dir("ssl/client-certs/atat.mil.crt"),
                relative_dir("ssl/client-certs/atat.mil.key"),
            )
        ):
            return self.client.get(self.server_api, cert=certs, allow_redirects=False)

    return RequestClient(server_api)


def test_log_in_with_cac(request_client):
    r = request_client.login()
    assert r.status_code == 302
    assert re.search("bearer-token", r.headers["Location"])


def test_log_in_fails_without_cac(request_client):
    r = request_client.login(certs=())
    assert r.status_code == 403


def test_log_in_with_revoked_certificate(request_client):
    certs=(
        relative_dir("ssl/client-certs/bad-atat.mil.crt"),
        relative_dir("ssl/client-certs/bad-atat.mil.key"),
    )
    r = request_client.login(certs)
    assert r.status_code == 403


def test_log_in_with_cac_redirects_with_token(request_client):
    response = request_client.login()
    location = response.headers['Location']
    token = re.search('bearer-token=([^;]+)', location)[1]
    assert len(location) < 2000 # ensure URL is under a safe limit
    assert response.status_code == 302
    assert is_token(token)
