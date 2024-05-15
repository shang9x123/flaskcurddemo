from datetime import datetime

class BaseModel:
    def __init__(self, created_at=None, **kwargs):
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.utcnow()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def json(self):
        data = dict(self.__dict__)
        return data