# Import installed packages
import requests
import re
# Import app code
from app.core import config


def test_log_in_with_cac():
    r = requests.get(f'https://{config.SERVER_NAME}/',
        headers={'X-Client-Verify': 'SUCCESS'},
        allow_redirects=False)
    assert r.status_code == 302
    assert re.search("www", r.headers['Location'])
