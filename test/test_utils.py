import pytest
from .helpers import DOD_SDN
import authnid.utils as utils

def test_parse_sdn():
    parsed = utils.parse_sdn(DOD_SDN)
    assert parsed.get('first_name') == 'ART'
    assert parsed.get('last_name') == 'GARFUNKEL'
    assert parsed.get('dod_id') == '5892460358'

def test_parse_bad_sdn():
    with pytest.raises(ValueError):
        utils.parse_sdn('this has nothing to do with anything')
    with pytest.raises(ValueError):
        utils.parse_sdn(None)
