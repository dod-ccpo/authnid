from flask import Blueprint

def new_api(name, import_name):
    return Blueprint(name, import_name)
