# -*- coding: utf-8 -*-

# Import installed packages
from flask import Flask, request, redirect, render_template
from .make_app import configured_app

app = configured_app()

@app.route('/')
def log_in_user():
    # FIXME: Find or create user based on the X-Ssl-Client-S-Dn header
    # TODO: Store/log the X-Ssl-Client-Cert in case it's needed?
    if request.environ.get('HTTP_X_SSL_CLIENT_VERIFY') == 'SUCCESS' and is_valid_certificate(request):
        s_dn = request.environ['HTTP_X_SSL_CLIENT_S_DN']
        return construct_redirect()
    else:
        template = render_template('not_authorized.html', atst_url=app.config['ATST_PASSTHROUGH'])
        response = app.make_response(template)
        response.status_code = 403

    return response

def is_valid_certificate(request):
    cert = request.environ.get('HTTP_X_SSL_CLIENT_CERT')
    if cert:
        result = app.crl_validator.validate(cert.encode())
        if not result:
            app.logger.info(app.crl_validator.errors[-1])
        return result
    else:
        return False

def construct_redirect():
    access_token = app.token_manager.token()
    url = f'{app.config["ATST_REDIRECT"]}?bearer-token={access_token}'
    return app.make_response(redirect(url))
