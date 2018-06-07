import re

def is_jwt(token):
    return re.match('\A[\w-]+\.[\w-]+\.[\w-]+\Z', token)

