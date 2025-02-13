import re

from marshmallow import Schema, fields

from flaskr.config.ma import ma
from flaskr.models import Room, RoomAccess
from flaskr.schemas.item import ItemListResponseSchema


class RoomInitialStepResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    code = ma.auto_field()


class RoomLastStepRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    code = ma.auto_field(required=True)
    passcode = ma.auto_field(
        required=True,
        validate=lambda x: bool(re.match(r'^\d{4}$', x))
    )


class RoomPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    code = ma.auto_field()


class RoomListResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    name = ma.auto_field()
    code = ma.auto_field()

    items = ma.Nested(ItemListResponseSchema, many=True)


class RoomValidateRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Room

    code = ma.auto_field()
    passcode = ma.auto_field()


class RoomValidateAccessCodeRequestSchema(Schema):
    room_code = fields.String(required=True)
    access_code = fields.String(required=True)


class RoomCodeAccessCodeResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RoomAccess

    access_code = ma.auto_field()
