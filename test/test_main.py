# Import installed packages
import requests
import re


def test_log_in_with_cac(server_api):
    r = requests.get(server_api,
        cert=(
            '/app/ssl/client-certs/atat.mil.crt',
            '/app/ssl/client-certs/atat.mil.key',
            ),
        allow_redirects=False
        )
    assert r.status_code == 302
    assert re.search("www", r.headers['Location'])

def test_log_in_fails_without_cac(server_api):
    r = requests.get(server_api, allow_redirects=False)
    assert r.status_code == 403
