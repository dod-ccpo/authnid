import os
from flask import Flask
from configparser import ConfigParser

config_defaults = {
    'PORT': 4567,
    'DEBUG': True,
    'TESTING': False,
    'ATST_REDIRECT': 'https://dev.www.atat.codes/log-in'
}

def make_app(config):
    app = Flask(__name__)
    app.config.update(config_defaults)
    app.config.update(config)

    return app

def make_config():
    CONFIG_FILENAME = os.path.join(
        os.path.dirname(__file__),
        '..',
        os.getenv('CONFIG_FILENAME', 'config.ini')
    )
    if os.path.exists(CONFIG_FILENAME):
        config = ConfigParser()
        config.optionxform = str
        config.read(CONFIG_FILENAME)

        return config._sections['default']
    else:

        return config_defaults

def configured_app():
    config = make_config()
    return make_app(config)
