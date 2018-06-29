import os
import re
import base64

DOD_SDN_INFO = {
        'first_name': 'ART',
        'last_name': 'GARFUNKEL',
        'dod_id': '5892460358'
    }
DOD_SDN = f"CN={DOD_SDN_INFO['last_name']}.{DOD_SDN_INFO['first_name']}.G.{DOD_SDN_INFO['dod_id']},OU=OTHER,OU=PKI,OU=DoD,O=U.S. Government,C=US"

def is_token(token):
    return re.match('\A[\w\-=]+\.[\w\-=]+\.[\w\-=]+\Z', token)

def relative_dir(path):
    return f'{os.getcwd()}/{path}'

