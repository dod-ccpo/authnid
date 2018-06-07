# Import installed packages
import requests
import re
from test.helpers import is_token


def test_log_in_with_cac(request_client):
    r = request_client.login()
    assert r.status_code == 302
    assert re.search("www", r.headers["Location"])


def test_log_in_fails_without_cac(request_client):
    r = request_client.login(certs=())
    assert r.status_code == 403


def test_log_in_with_revoked_certificate(request_client):
    certs=(
        "/app/ssl/client-certs/bad-atat.mil.crt",
        "/app/ssl/client-certs/bad-atat.mil.key",
    )
    r = request_client.login(certs)
    assert r.status_code == 403


def test_log_in_with_cac_sets_token(request_client):
    r = request_client.login()
    # requests considers the value of our Set-Cookie header to be invalid and
    # so does not set it in the CookieJar (i.e., r.cookies); instead we extract
    # from the response headers
    # https://github.com/requests/requests/issues/4414
    set_cookie = r.headers.get('Set-Cookie')
    token = re.match('bearer-token=([^;]+)', set_cookie)[1]
    assert is_token(token)
