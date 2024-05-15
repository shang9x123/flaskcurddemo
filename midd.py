from flask import Blueprint,request
from middleware import checkheader
import json
middle = Blueprint('middle', __name__)


@middle.before_request
def before_request():
    # thêm bảo mật với api key
    token = request.headers.get('token')
    check = checkheader.check_headers(token)
    if (check == False):
        return json.dumps({
            'status': 0,
            'message': 'Invalid token',
        })
