# Import installed packages
import pytest
import re
from authnid.crl.validator import Validator
import authnid.crl.util as util


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
    location = 'ssl/client-certs/client-ca.der.crl'
    validator = Validator(crl_locations=[location], store=MockX509Store())
    assert len(validator.store.crls) == 1

def test_can_build_trusted_root_list():
    location = 'ssl/server-certs/ca-chain.pem'
    validator = Validator(roots=[location], store=MockX509Store())
    with open(location) as f:
        content = f.read()
        assert len(validator.store.certs) == content.count('BEGIN CERT')

def test_can_validate_certificate():
    validator = Validator(
            roots=['ssl/server-certs/ca-chain.pem'],
            crl_locations=['ssl/client-certs/client-ca.der.crl']
            )
    good_cert = open('ssl/client-certs/atat.mil.crt', 'rb').read()
    bad_cert = open('ssl/client-certs/bad-atat.mil.crt', 'rb').read()
    assert validator.validate(good_cert)
    assert validator.validate(bad_cert) == False


def test_parse_disa_pki_list():
    with open('test/fixtures/disa-pki.html') as disa:
        disa_html = disa.read()
        crl_list = util.crl_list_from_disa_html(disa_html)
        href_matches = re.findall('DOD(ROOT|EMAIL|ID)?CA', disa_html)
        assert len(crl_list) > 0
        assert len(crl_list) == len(href_matches)

class MockStreamingResponse():
    def __init__(self, content_chunks):
        self.content_chunks = content_chunks

    def iter_content(self, chunk_size=0):
        return self.content_chunks

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

def test_write_crls(tmpdir, monkeypatch):
    monkeypatch.setattr('requests.get', lambda u, **kwargs: MockStreamingResponse([b'it worked']))
    crl_list = ['crl_1']
    util.write_crls(tmpdir, crl_list)
    assert [p.basename for p in tmpdir.listdir()] == crl_list
    assert [p.read() for p in tmpdir.listdir()] == ['it worked']
