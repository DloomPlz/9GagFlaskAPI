from . import api

@api.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'