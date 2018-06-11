import re
import base64

def is_token(token):
    return re.match('\A[\w\-=]+\Z', token)

