import pytest
import re
from authnid.make_app import make_config
from authnid.make_db import make_db
from authnid.user_repo import UserRepo

@pytest.fixture(scope="module")
def db():
    return make_db(make_config())

@pytest.fixture(scope="module")
def repo():
    return UserRepo(db())

@pytest.fixture(autouse=True)
def reset(db):
    db.execute("BEGIN;")
    yield
    db.execute("ROLLBACK;")

def test_add_user(repo):
    uuid = repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert re.match('[\w-]+', uuid)

def test_get_user(repo):
    uuid = repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    user = repo.get_user(uuid)
    assert user.get('id') == uuid
    assert user.get('email') == 'artgarfunkel@s_and_g.com'
    assert user.get('dod_id') == '123456'

def test_has_user(repo):
    uuid = repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert repo.has_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert not repo.has_user(email='simon@s_and_g.com', dod_id='123456')
