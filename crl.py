import sys
import os
from asn1crypto import pem
from certvalidator import CertificateValidator, ValidationContext, errors

trust_roots = []
with open('ssl/server-certs/ca-chain.pem', 'rb') as f:
    for _, _, der_bytes in pem.unarmor(f.read(), multiple=True):
        trust_roots.append(der_bytes)

with open('ssl/client-certs/bad-atat.mil.crt', 'rb') as f:
    end_entity_cert = f.read()

crls = []
for filename in os.listdir('crl'):
    with open(f'crl/{filename}', 'rb') as crl:
        crls.append(crl.read())

def validate(cert):
    with open(cert, 'rb') as f:
        end_entity_cert = f.read()
        context = ValidationContext(crls=crls, trust_roots=trust_roots, revocation_mode="require")
        validator = CertificateValidator(end_entity_cert, validation_context=context)
        try:
            validator.validate_usage(set([]))
            print(f'{cert} is valid! HOORAY!')
        except errors.RevokedError:
            print(f'{cert} is not valid!!!')

validate('ssl/client-certs/atat.mil.crt')
validate('ssl/client-certs/bad-atat.mil.crt')
