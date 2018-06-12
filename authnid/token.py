import time
import hashlib
import hmac
import base64
import binascii

class TokenManager():
    def __init__(self, secret):
        self._secret = secret.encode()

    # stub user ID until we implement it
    def token(self, user_id=10000):
        payload = f'{user_id}:{self._timestamp()}'
        return self._encode(payload)

    def validate(self, token):
        try:
            decoded = base64.urlsafe_b64decode(token).decode()
            parts = decoded.split(':', 1)
            recoded = self._encode(parts[1])
            return hmac.compare_digest(token, recoded)
        except binascii.Error:
            return False

    def _timestamp(self):
        return str(int(time.time()))

    def _encode(self, payload):
        payload_bytes = payload.encode()
        hashed = hmac.new(self._secret, payload_bytes, hashlib.sha256)
        hexed = binascii.hexlify(hashed.digest())
        return base64.urlsafe_b64encode(hexed + b':' + payload_bytes).decode()
