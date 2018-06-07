from authnid.api.common import new_api

def make_api():
    api = new_api('api_v1', 'api_v1')

    @api.route('/validate')
    def validate():
        return 'hello world'

    return api
