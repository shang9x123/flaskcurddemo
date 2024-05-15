from flask import Flask, jsonify, request
from markupsafe import escape
from pymongo import MongoClient
import json
from middleware import checkheader
from controller.postcontroller import *
from controller.taskcontroller import *
from models.task import *
from pprint import pprint
from flask_caching import Cache

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['UPLOAD_FOLDER'] = './uploads'

cache = Cache(app)

app.register_blueprint(post, url_prefix='/post')
app.register_blueprint(taskcontroller, url_prefix='/task')

@app.before_request
def before_request():
    # thêm bảo mật với api key
    token = request.headers.get('token')
    check = checkheader.check_headers(token)
    if (check == False):
        return json.dumps({
            'status': 0,
            'message': 'Invalid token',
        })


@app.route('/', methods=['GET'])
@cache.cached(timeout=400)
def index():
    return 'request %s'


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(db.user.find({}, {"_id": 0}))
    json_str = json.dumps(tasks, ensure_ascii=False).encode('utf-8')
    return json_str
    # return jsonify({"tasks": json_str})


@app.route('/tasks/findbyname/<string:slug>', methods=['GET'])
@cache.cached(timeout=200)
def get_tasks_slug(slug=None):
    tasks = list(db.user.find({'slug': slug}, {"_id": 0}))
    json_str = json.dumps(tasks, ensure_ascii=False).encode('utf-8')
    return json_str
    # return jsonify({"tasks": json_str})


@app.route('/tasks', methods=['POST'])
def add_task():
    name = request.form.get('name')
    slug = request.form.get('slug')
    new_task = {
        "name": name,
        "slug": slug,
    }
    result = db.tasks.insert_one(new_task)
    if result.inserted_id:
        return 'Task added successfully'
    else:
        return 'Failed to add task'


@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task_data = request.get_json()
    db.tasks.update_one({"_id": id}, {"$set": task_data})
    return 'Task updated successfully'


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    db.tasks.delete_one({"_id": id})
    return 'Task deleted successfully'


if __name__ == '__main__':
    app.run()
