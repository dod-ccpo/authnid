import pytest
import re
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
