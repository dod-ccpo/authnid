import pytest
import re
from .helpers import DOD_SDN_INFO
from authnid.make_app import make_config
from authnid.make_db import make_db
from authnid.user_repo import UserRepo

def test_add_user(user_repo):
    uuid = user_repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert re.match('[\w-]+', uuid)

def test_get_user(user_repo):
    uuid = user_repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    user = user_repo.get_user(id=uuid)
    assert user.get('id') == uuid
    assert user.get('email') == 'artgarfunkel@s_and_g.com'
    assert user.get('dod_id') == '123456'

def test_has_user(user_repo):
    uuid = user_repo.add_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert user_repo.has_user(email='artgarfunkel@s_and_g.com', dod_id='123456')
    assert not user_repo.has_user(email='simon@s_and_g.com', dod_id='123456')

def test_ensure_user_exists_new_user(user_repo):
    c = user_repo.count()
    uuid = user_repo.ensure_user_exists(**DOD_SDN_INFO)
    assert user_repo.count() == c+1
    assert re.match('^[\w-]+', uuid)

def test_ensure_user_exists_existing_user(user_repo):
    user_repo.add_user(**DOD_SDN_INFO)
    c = user_repo.count()
    uuid = user_repo.ensure_user_exists(**DOD_SDN_INFO)
    assert user_repo.count() == c
    assert re.match('^[\w-]+', uuid)
