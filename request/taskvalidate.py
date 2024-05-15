from marshmallow import validate,Schema,fields
class TaskValidation(Schema):
    name = fields.Str(required=True,validate= validate.Length(min=3,max=100))
    slug = fields.Str(required=True,validate= validate.Length(min=3,max=100))
    age = fields.Int(required=False,validate=validate.Range(min=1,max=100))
