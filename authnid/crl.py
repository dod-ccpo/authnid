import sys
import os
import re
from OpenSSL import crypto, SSL


class Validator():
    def __init__(self, crl_locations=[], roots=[], store=crypto.X509Store()):
        self.store = store
        self.errors = []
        self._add_crls(crl_locations)
        self._add_roots(roots)
        self.store.set_flags(crypto.X509StoreFlags.CRL_CHECK)

    def _add_crls(self, locations):
        for filename in locations:
            with open(filename, 'rb') as crl_file:
                crl = crypto.load_crl(crypto.FILETYPE_PEM, crl_file.read())
                self._add_carefully('add_crl', crl)

    def _add_roots(self, roots):
        for filename in roots:
            with open(filename, 'rb') as f:
                pems = f.read().decode()
                raw_cas = re.split('(?<=END CERTIFICATE-----)\n(?=-----BEGIN CERTIFICATE)', pems)
                for raw_ca in raw_cas:
                    ca = crypto.load_certificate(crypto.FILETYPE_PEM, raw_ca)
                    self._add_carefully('add_cert', ca)

    # in testing, it seems that openssl is maintaining a local cache of certs
    # in a hash table and throws errors if you try to add redundant certs or
    # CRLs. For now, we catch and ignore that error with great specificity.
    def _add_carefully(self, method_name, obj):
        try:
            getattr(self.store, method_name)(obj)
        except crypto.Error as error:
            if self._is_preloaded_error(error):
                pass
            else:
                raise error

    PRELOADED_CRL = ([('x509 certificate routines', 'X509_STORE_add_crl', 'cert already in hash table')],)
    PRELOADED_CERT = ([('x509 certificate routines', 'X509_STORE_add_cert', 'cert already in hash table')],)
    def _is_preloaded_error(self, error):
        return error.args == self.PRELOADED_CRL or error.args == self.PRELOADED_CERT

    def validate(self, cert):
        parsed = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        context = crypto.X509StoreContext(self.store, parsed)
        try:
            context.verify_certificate()
            return True
        except crypto.X509StoreContextError as err:
            self.errors.append(err)
            return False

