from flask import Blueprint
post = Blueprint('post', __name__)
@post.route('/post/index',methods=['GET', 'POST'])
def index():
    return "Post index"