import jwt

class JWTManager():
    def __init__(self, secret):
        self._secret = secret

    def token(self):
        return jwt.encode({'some': 'payload'}, self._secret).decode('utf-8')
