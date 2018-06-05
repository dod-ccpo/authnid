import sys
import os
from asn1crypto import pem
from certvalidator import CertificateValidator, ValidationContext, errors

class Validator():
    def __init__(self, crl_locations=[], roots=[]):
        crls = self._read_crls(crl_locations)
        self.trust_roots = self._read_roots(roots)
        self.context = ValidationContext(crls=crls, trust_roots=self.trust_roots, revocation_mode="require")

    def _read_crls(self, locations):
        crls = []
        for filename in locations:
            with open(filename, 'rb') as crl:
                crls.append(crl.read())
        return crls

    def _read_roots(self, roots):
        trust_roots = []
        for filename in roots:
            with open(filename, 'rb') as f:
                for _, _, der_bytes in pem.unarmor(f.read(), multiple=True):
                    trust_roots.append(der_bytes)
        return trust_roots

    def validate(self, cert):
        validator = CertificateValidator(cert, validation_context=self.context)
        try:
            validator.validate_usage(set([]))
            return True
        except errors.RevokedError:
            return False

