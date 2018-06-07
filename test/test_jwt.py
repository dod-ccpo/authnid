import re
from authnid.jwt import JWTManager

def test_can_build_jwt():
    jwt_maker = JWTManager('some-secret')
    token = jwt_maker.token()
    assert re.match('\A[\w-]+\.[\w-]+\.[\w-]+\Z', token)
