# -*- coding: utf-8 -*-

# Import installed packages
import pathlib
from flask import Flask, request, redirect, render_template
from .make_app import configured_app
from .crl import Validator

app = configured_app()

crl_locations = []
for filename in pathlib.Path(app.config['CRL_DIRECTORY']).glob('*'):
    crl_locations.append(filename.absolute())

validator = Validator(roots=[app.config['CA_CHAIN']], crl_locations=crl_locations)

@app.route('/')
def log_in_user():
    # FIXME: Find or create user based on the X-Ssl-Client-S-Dn header
    # TODO: Store/log the X-Ssl-Client-Cert in case it's needed?
    redirect_url = app.config['ATST_REDIRECT']

    if request.environ.get('HTTP_X_SSL_CLIENT_VERIFY') == 'SUCCESS' and is_valid_certificate(request):
        response = app.make_response(redirect(redirect_url))
    else:
        template = render_template('not_authorized.html', atst_url=redirect_url)
        response = app.make_response(template)
        response.status_code = 403

    return response

def is_valid_certificate(request):
    cert = request.environ.get('HTTP_X_SSL_CLIENT_CERT')
    if cert:
        return validator.validate(cert.encode())
    else:
        return False
