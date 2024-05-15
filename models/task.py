from pymongo import MongoClient
from datetime import datetime
from models.basemodel import BaseModel

# client = MongoClient('mongodb://localhost:27017')
client = MongoClient('mongodb+srv://anhhien:Ahiendam123@server1.sicpm.mongodb.net/?retryWrites=true&w=majority&appName=Server1')
db = client['flask']


class Task(BaseModel):
    def __init__(self, name, slug, status, created_at=None):
        super().__init__(created_at, name=name, slug=slug, status=status)

    @staticmethod
    def from_dict(task_dict):
        return Task(
            name=task_dict.get('title'),
            slug=task_dict.get('slug'),
            status=task_dict.get('status'),
            created_at=task_dict.get('created_at', datetime.utcnow())
        )
    @staticmethod
    def to_dict(task):
        return task.__dict__