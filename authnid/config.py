import os

class Config():
    DEBUG = False
    TESTING = False
    PORT = os.getenv('AUTHNID_PORT') or 80
    ATST_REDIRECT = 'https://dev.www.atat.codes/log-in'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

def config_for_env():
    env = os.getenv('FLASK_ENV')
    return {
            'testing': TestingConfig,
            'development': DevelopmentConfig,
            'production': ProductionConfig,
            }.get(env, DevelopmentConfig)

def apply_config(config_obj):
    config_obj.from_object(config_for_env())
    if os.path.exists('authnid.cfg'):
        config_obj.from_pyfile('../authnid.cfg')
