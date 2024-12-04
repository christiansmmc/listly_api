from flask import request
from marshmallow import ValidationError

from flaskr.schemas.error import ErrorSchema


def validate_schema(schema_class):
    schema = schema_class()
    try:
        return schema.load(request.get_json())
    except ValidationError as err:
        error_schema = ErrorSchema()
        return error_schema.dump({
            "status": 400,
            "message": "Invalid request data",
            "errors": err.messages
        }), 400
