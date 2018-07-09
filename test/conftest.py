import pytest
import requests
from authnid.make_app import make_app, make_config
from authnid.make_db import connect_db, make_cursor
from authnid.user_repo import UserRepo
from .helpers import relative_dir, DOD_SDN_INFO


@pytest.fixture(scope='module')
def app():
    config = make_config()
    return make_app(config)


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_repo(database):
    return UserRepo(database)

@pytest.fixture(scope="module")
def database():
    db_uri = make_config()['DATABASE_URI']
    connection = connect_db(db_uri)
    yield make_cursor(connection)
    connection.close()

@pytest.fixture(scope='function', autouse=True)
def reset(database):
    yield
    database.execute("TRUNCATE users;")
    database.connection.commit()

@pytest.fixture
def dod_user():
    user_info = DOD_SDN_INFO.copy()
    return user_info
