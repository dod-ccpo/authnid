import re

def is_token(token):
    return re.match('\A[\w-]+\.[\w-]+\.[\w-]+\Z', token)

