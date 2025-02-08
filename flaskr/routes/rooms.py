from flask import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flaskr.models import Room, RoomAccess
from flaskr.schemas.room import RoomInitialStepResponseSchema, RoomLastStepRequestSchema, RoomPublicSchema, \
    RoomListResponseSchema, RoomValidateRequestSchema, RoomValidateAccessCodeRequestSchema, \
    RoomCodeAccessCodeResponseSchema
from flaskr.schemas.validation import validate_schema
from flaskr.services.rooms import RoomService
from flaskr.utils import get_4_digits_code, get_current_time, validate_jwt_room_code, get_access_code

rooms_bp = Blueprint('rooms', __name__, url_prefix='/api/v1/rooms')


@rooms_bp.post('/initial-step')
def initial_step_create_room():
    room_code = RoomService.generate_unique_room_code()

    room = Room(code=room_code, passcode=get_4_digits_code())
    room.save()

    room_schema = RoomInitialStepResponseSchema()
    return room_schema.dump(room), 201


@rooms_bp.post('/last-step')
def last_step_create_room():
    request_body = validate_schema(RoomLastStepRequestSchema)
    room = Room.query.filter_by(code=request_body['code']).first()

    if not room:
        abort(404, description='Room not found')

    if room.active:
        abort(400, 'Room already created')

    room.passcode = request_body['passcode']
    room.active = True
    room.save()

    room_schema = RoomPublicSchema()
    return room_schema.dump(room), 201


@rooms_bp.delete('<string:room_code>')
@jwt_required()
def delete_room(room_code):
    jwt_room_code = get_jwt_identity()

    validate_jwt_room_code(jwt_room_code, room_code, 204, None)

    room = Room.query.filter_by(code=jwt_room_code).first()

    if not room:
        return {}, 204

    room.deleted_at = get_current_time()
    room.save()
    return {}, 204


@rooms_bp.post('/validate')
def validate_room():
    request_body = validate_schema(RoomValidateRequestSchema)
    room = RoomService.validate_room(request_body['code'], request_body['passcode'])

    access_token = create_access_token(identity=room.code)
    return {"access_token": access_token}, 200


@rooms_bp.post('/validate/access-code')
def validate_room_access_code():
    request_body = validate_schema(RoomValidateAccessCodeRequestSchema)
    room = RoomService.validate_room_access_code(request_body['room_code'], request_body['access_code'])

    access_token = create_access_token(identity=room.code)
    return {"access_token": access_token}, 200


@rooms_bp.get('/<string:room_code>')
@jwt_required()
def get_room(room_code):
    jwt_room_code = get_jwt_identity()
    validate_jwt_room_code(jwt_room_code, room_code, 404, "Room not found")

    room = RoomService.find_room_by_code(jwt_room_code)

    room_schema = RoomListResponseSchema()
    return room_schema.dump(room), 200


@rooms_bp.get('/<string:room_code>/generate-access-code')
@jwt_required()
def generate_access_code(room_code):
    jwt_room_code = get_jwt_identity()
    validate_jwt_room_code(jwt_room_code, room_code, 404, "Room not found")

    room = RoomService.find_room_by_code(jwt_room_code)
    room_access = RoomAccess(access_code=get_access_code(), room=room)
    room_access.save()

    room_access_schema = RoomCodeAccessCodeResponseSchema()
    return room_access_schema.dump(room_access), 200
