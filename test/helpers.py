import os
import re
import base64

def is_token(token):
    return re.match('\A[\w\-=]+\.[\w\-=]+\.[\w\-=]+\Z', token)

def relative_dir(path):
    return f'{os.getcwd()}/{path}'

