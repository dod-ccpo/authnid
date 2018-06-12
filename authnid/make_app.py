import os
from flask import Flask
from configparser import ConfigParser

config_defaults = {
    'PORT': 4567,
    'DEBUG': True,
    'TESTING': False,
    'ATST_REDIRECT': 'https://www.atat.codes/home',
    'CRL_DIRECTORY': 'crl',
    'CA_CHAIN': '/app/ssl/server-certs/ca-chain.pem'
}

def make_app(config):
    app = Flask(__name__)
    app.config.update(config_defaults)
    app.config.update(config)

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
