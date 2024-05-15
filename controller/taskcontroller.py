from flask import Flask, json, request, Blueprint
from models.task import Task, db
from marshmallow.exceptions import ValidationError

taskcontroller = Blueprint('task', import_name='task')
from pprint import pprint
from request.taskvalidate import TaskValidation


@taskcontroller.route('/')
def index():
    task_data = list(db.tasks.find({}, {"_id": 0}))
    return json.dumps({
        'status': 1,
        'data': task_data,
    })


@taskcontroller.route('/create', methods=['POST'])
def create():
    try:
        name = request.form.get('name', 'default')
        slug = request.form.get('slug')
        taskva = TaskValidation()
        taskva.load({
            'name': name,
            'slug': slug,
        })
        # check slug nếu có thì ko tạo
        # check_slug = db.tasks.find({'slug': slug})
        check_slug = db.tasks.count_documents({'slug': slug})
        print(check_slug)
        # kiểm tra đã có data thì không cho import tiếp
        if (check_slug > 0):
            return json.dumps({'stautus': 0, 'message': 'đã có'}, ensure_ascii=False).encode('utf-8')
        task_data = Task(name, slug, 1)
        result = db.tasks.insert_one(task_data.json())
        if result.inserted_id:
            return 'Task added successfully'
        else:
            return 'Failed to add task'
    except ValidationError as err:
            return json.dumps({'message': 'Validation error', 'errors': err.messages})
