from flask import Blueprint, request, redirect, render_template
from flask import current_app as app
from .utils import parse_sdn
from .make_db import connect_db, make_cursor
from .user_repo import UserRepo

root = Blueprint('home', __name__)

@root.route('/')
def log_in_user():
    # FIXME: Find or create user based on the X-Ssl-Client-S-Dn header
    # TODO: Store/log the X-Ssl-Client-Cert in case it's needed?
    if request.environ.get('HTTP_X_SSL_CLIENT_VERIFY') == 'SUCCESS' and is_valid_certificate(request):
        sdn = request.environ.get('HTTP_X_SSL_CLIENT_S_DN')
        ensure_user_exists(sdn)
        return construct_redirect()
    else:
        template = render_template('not_authorized.html', atst_url=app.config['ATST_PASSTHROUGH'])
        response = app.make_response(template)
        response.status_code = 403

    return response

@root.before_request
def before_request():
    app.db = connect_db(app.db_uri)
    cursor = make_cursor(app.db)
    autocommit = app.config['ENV'] != 'test'
    app.user_repo = UserRepo(app.db.cursor(), autocommit=autocommit)

@root.teardown_request
def teardown_request(exception):
    db = getattr(app, 'db', None)
    if db is not None:
        db.close()

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

# TODO: error handling for bad SDN
# TODO: return uuid
def ensure_user_exists(sdn):
    sdn_parts = parse_sdn(sdn)
    if app.user_repo.has_user(**sdn_parts):
        return
    else:
        app.user_repo.add_user(**sdn_parts)
