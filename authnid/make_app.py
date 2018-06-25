import os
import pathlib
from flask import Flask
from configparser import ConfigParser
from .crl import Validator
from .token import TokenManager
from .root import root
from .api.v1.routes import make_api as make_api_v1
from .make_db import make_db
from .user_repo import UserRepo

config_defaults = {
    "PORT": 4567,
    "DEBUG": True,
    "TESTING": False,
    "ATST_REDIRECT": "https://www.atat.codes/home",
    "CRL_DIRECTORY": "crl",
    "CA_CHAIN": "ssl/server-certs/ca-chain.pem",
    "TOKEN_SECRET": "abc-123",
}


def make_app(config):
    app = Flask(__name__)
    app.config.update(config_defaults)
    app.config.update(config)

    db = make_db(config)

    _make_user_repo(app, db)
    _make_token_manager(app)
    _make_crl_validator(app)
    # apply root route
    app.register_blueprint(root)
    _apply_apis(app)

    return app


def make_config():
    BASE_CONFIG_FILENAME = os.path.join(
        os.path.dirname(__file__),
        '../config/base.ini',
    )
    ENV_CONFIG_FILENAME = os.path.join(
        os.path.dirname(__file__),
        '../config/',
        '{}.ini'.format(os.getenv('FLASK_ENV', 'dev').lower())
    )
    config = ConfigParser()
    config.optionxform = str
    config.read([BASE_CONFIG_FILENAME, ENV_CONFIG_FILENAME])

    return config._sections['default']


def configured_app():
    config = make_config()
    return make_app(config)


def _apply_apis(app):
    app.register_blueprint(make_api_v1(app.token_manager), url_prefix="/api/v1")


def _make_crl_validator(app):
    crl_locations = []
    for filename in pathlib.Path(app.config["CRL_DIRECTORY"]).glob("*"):
        crl_locations.append(filename.absolute())
    app.crl_validator = Validator(
        roots=[app.config["CA_CHAIN"]], crl_locations=crl_locations
    )


def _make_token_manager(app):
    app.token_manager = TokenManager(app.config.get("TOKEN_SECRET"))

def _make_user_repo(app, db):
    app.user_repo = UserRepo(db)
