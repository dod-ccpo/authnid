# Import installed packages
import pytest
from authnid.crl import Validator


class MockX509Store():
    def __init__(self):
        self.crls = []
        self.certs = []

    def add_crl(self, crl):
        self.crls.append(crl)

    def add_cert(self, cert):
        self.certs.append(cert)

    def set_flags(self, flag):
        pass

def test_can_build_crl_list(monkeypatch):
    location = 'ssl/client-certs/client-ca.pem.crl'
    validator = Validator(crl_locations=[location], store=MockX509Store())
    assert len(validator.store.crls) == 1

def test_can_build_trusted_root_list():
    location = 'ssl/server-certs/ca-chain.pem'
    validator = Validator(roots=[location], store=MockX509Store())
    assert len(validator.store.certs) > 0

def test_can_validate_certificate():
    validator = Validator(
            roots=['ssl/server-certs/ca-chain.pem'],
            crl_locations=['ssl/client-certs/client-ca.pem.crl']
            )
    good_cert = open('ssl/client-certs/atat.mil.crt', 'rb').read()
    bad_cert = open('ssl/client-certs/bad-atat.mil.crt', 'rb').read()
    assert validator.validate(good_cert)
    assert validator.validate(bad_cert) == False
