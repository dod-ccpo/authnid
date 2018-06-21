import pytest
import authnid.utils as utils

DOD_SDN = 'CN=GARFUNKEL.ART.G.5892460358,OU=OTHER,OU=PKI,OU=DoD,O=U.S. Government,C=US'

def test_parse_sdn():
    parsed = utils.parse_sdn(DOD_SDN)
    assert parsed.get('first_name') == 'ART'
    assert parsed.get('last_name') == 'GARFUNKEL'
    assert parsed.get('dod_id') == '5892460358'

def test_parse_bad_sdn():
    with pytest.raises(ValueError):
        utils.parse_sdn('this has nothing to do with anything')
