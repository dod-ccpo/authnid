from flask import request, jsonify
from flask import current_app as app
from authnid.api.common import new_api

def make_api(token_manager):
    api = new_api('api_v1', 'api_v1')

    @api.route('/validate', methods=['POST'])
    def validate():
        token = request.get_json()['token']
        # TODO: error handling for bad tokens
        if token_manager.validate(token):
            parts = token_manager.parse(token)
            user = app.user_repo.get_user(id=parts['id'])
            return jsonify({'status': 'success', 'user': dict(user)})
        else:
            resp = jsonify({'status': 'error'})
            resp.status_code = 401
            return resp

    return api
