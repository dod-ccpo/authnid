# Import installed packages
from authnid.crl import Validator
from certvalidator import ValidationContext


def test_can_build_crl_list():
    location = 'ssl/client-certs/client-ca.der.crl'
    validator = Validator(crl_locations=[location])
    assert len(validator.context.crls) == 1

def test_can_build_trusted_root_list():
    location = 'ssl/server-certs/ca-chain.pem'
    validator = Validator(roots=[location])
    assert len(validator.trust_roots) > 0

def test_can_validate_certificate():
    validator = Validator(
            roots=['ssl/server-certs/ca-chain.pem'],
            crl_locations=['ssl/client-certs/client-ca.der.crl']
            )
    good_cert = open('ssl/client-certs/atat.mil.crt', 'rb').read()
    bad_cert = open('ssl/client-certs/bad-atat.mil.crt', 'rb').read()
    assert validator.validate(good_cert)
    assert validator.validate(bad_cert) == False
