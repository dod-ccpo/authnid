# -*- coding: utf-8 -*-

# Import installed packages
from flask import Flask, request, redirect, render_template
from .make_app import configured_app

app = configured_app()

@app.route('/')
def log_in_user():
    # FIXME: Find or create user based on the X-Ssl-Client-S-Dn header
    # TODO: Store/log the X-Ssl-Client-Cert in case it's needed?
    redirect_url = app.config['ATST_REDIRECT']

    if request.environ.get('HTTP_X_SSL_CLIENT_VERIFY') == 'SUCCESS' and is_valid_certificate(request):
        response = app.make_response(redirect(redirect_url))
        set_bearer_token(response)
    else:
        template = render_template('not_authorized.html', atst_url=redirect_url)
        response = app.make_response(template)
        response.status_code = 403

    return response

def is_valid_certificate(request):
    cert = request.environ.get('HTTP_X_SSL_CLIENT_CERT')
    if cert:
        return app.crl_validator.validate(cert.encode())
    else:
        return False

def set_bearer_token(response):
    access_token = app.token_manager.token()
    response.set_cookie('bearer-token', value=access_token,
            domain='.atat.codes', secure=True)
