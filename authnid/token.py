import time
import hashlib
import hmac
import base64

JOIN_CHAR = '.'

class TokenManager():
    def __init__(self, secret):
        self._secret = secret.encode()

    # stub user ID until we implement it
    def token(self, user_id):
        payload = f'{user_id}{JOIN_CHAR}{self._timestamp()}'
        return self._encode(payload)

    def validate(self, token):
        parts = token.split(JOIN_CHAR)
        if len(parts) != 3:
            return False
        recoded = self._encode(JOIN_CHAR.join(parts[1:]))
        return self._check_timestamp(parts[2]) and hmac.compare_digest(token, recoded)

    def _check_timestamp(self, timestamp):
        return abs(self._timestamp() - int(timestamp)) <= 2

    def _timestamp(self):
        return int(time.time())

    def _encode(self, payload):
        payload_bytes = payload.encode()
        hashed = hmac.new(self._secret, payload_bytes, hashlib.sha256)
        url_digest = base64.urlsafe_b64encode(hashed.digest()).decode()
        return url_digest + JOIN_CHAR + payload
