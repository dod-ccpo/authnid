from flask import request, jsonify
from authnid.api.common import new_api

def make_api(token_manager):
    api = new_api('api_v1', 'api_v1')

    @api.route('/validate', methods=['POST'])
    def validate():
        token = request.get_json()['token']
        if token_manager.validate(token):
            return jsonify({'status': 'success'})
        else:
            resp = jsonify({'status': 'error'})
            resp.status_code = 401
            return resp

    return api
