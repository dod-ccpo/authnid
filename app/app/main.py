# -*- coding: utf-8 -*-

from datetime import timedelta

# Import installed packages
from flask import Flask, request, redirect, render_template
from flask_jwt_extended import create_access_token

from app.core import config
from app.core.database import db_session
from app.models.user import User

# Import app code
app = Flask(__name__)

# Setup app
from .core import app_setup  # noqa

@app.route('/')
def log_in_user():
    # FIXME: Find or create user based on the X-Ssl-Client-S-Dn header
    # TODO: Store/log the X-Ssl-Client-Cert in case it's needed?
    user = db_session.query(User).first()
    access_token_expires = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        identity=user.id, expires_delta=access_token_expires)
    redirect_url = 'https://dev.www.atat.codes/log-in'

    if request.headers.get('X-Client-Verify') == 'SUCCESS':
        response = app.make_response(redirect(redirect_url))
    else:
        template = render_template('not_authorized.html', atst_url=redirect_url)
        response = app.make_response(template)
        response.status_code = 403

    response.set_cookie('bearer-token', value=access_token,
        domain='.atat.codes', secure=True)
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
