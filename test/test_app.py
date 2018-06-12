# Import installed packages
import requests
import re
from test.helpers import is_token, relative_dir


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
