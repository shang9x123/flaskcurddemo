from pymongo import MongoClient
from datetime import datetime
from models.basemodel import BaseModel

client = MongoClient('mongodb://localhost:27017')
db = client['flask']


class Task(BaseModel):
    def __init__(self, title, description, status, created_at=None):
        super().__init__(created_at, title=title, description=description, status=status)

    @staticmethod
    def from_dict(task_dict):
        return Task(
            title=task_dict.get('title'),
            description=task_dict.get('description'),
            status=task_dict.get('status'),
            created_at=task_dict.get('created_at', datetime.utcnow())
        )
    @staticmethod
    def to_dict(task):
        return task.__dict__