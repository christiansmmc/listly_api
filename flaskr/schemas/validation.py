from flask import request, abort
from marshmallow import ValidationError


def validate_schema(schema_class):
    schema = schema_class()
    try:
        return schema.load(request.get_json())
    except ValidationError as err:
        abort(400, err.messages)
