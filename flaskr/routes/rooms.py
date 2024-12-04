from flask import Blueprint

from flaskr.models import Room, Item
from flaskr.schemas.error import ErrorSchema
from flaskr.schemas.item import ItemCreateRequestSchema
from flaskr.schemas.room import RoomInitialStepResponseSchema, RoomLastStepRequestSchema, RoomPublicSchema, \
    RoomListResponseSchema
from flaskr.schemas.validation import validate_schema
from flaskr.services.rooms import RoomService
from flaskr.utils import get_4_digits_code, get_current_time, get_room_passcode_header

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
    validation_result = validate_schema(RoomLastStepRequestSchema)
    if isinstance(validation_result, tuple):
        return validation_result

    request_body = validation_result

    room = Room.query.filter_by(code=request_body['code']).first()

    if not room:
        error_schema = ErrorSchema()
        return error_schema.dump({
            "status": 404,
            "message": "Room not found"
        }), 400

    if room.active:
        error_schema = ErrorSchema()
        return error_schema.dump({
            "status": 400,
            "message": "Room already created"
        }), 400

    room.passcode = request_body['passcode']
    room.active = True
    room.save()

    room_schema = RoomPublicSchema()
    return room_schema.dump(room), 201


@rooms_bp.delete('<string:room_code>')
def delete_room(room_code):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    room = Room.query.filter_by(code=room_code, passcode=room_passcode).first()

    if not room:
        return {}, 204

    room.deleted_at = get_current_time()
    room.save()
    return {}, 204


@rooms_bp.get('/<string:room_code>')
def get_room(room_code):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    room = RoomService.find_room_by_code(room_code, room_passcode)
    if isinstance(room, tuple):
        return room

    room_schema = RoomListResponseSchema()
    return room_schema.dump(room), 200


#
# ITEMS
#

@rooms_bp.post('/<string:room_code>/items')
def add_item(room_code):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    request_body = validate_schema(ItemCreateRequestSchema)
    if isinstance(request_body, tuple):
        return request_body

    print(room_code, room_passcode)

    room = RoomService.find_room_by_code(room_code, room_passcode)
    if isinstance(room, tuple):
        return room

    #     TODO add category
    item = Item(name=request_body['name'], room_id=room.id)
    item.save()

    return {}, 201


@rooms_bp.delete('/<string:room_code>/items/<int:item_id>')
def delete_item(room_code, item_id):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    room = Room.query.filter_by(code=room_code, passcode=room_passcode).first()

    if not room:
        return {}, 204

    if not room.active or room.deleted_at is not None:
        return {}, 204

    item = Item.query.filter_by(room_id=room.id, id=item_id).first()

    if not item:
        return {}, 204

    item.delete()

    return {}, 204


@rooms_bp.patch('/<string:room_code>/items/<int:item_id>')
def check_item(room_code, item_id):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    room = RoomService.find_room_by_code(room_code, room_passcode)
    if isinstance(room, tuple):
        return room

    item = Item.query.filter_by(room_id=room.id, id=item_id).first()

    if not item:
        error_schema = ErrorSchema()
        return error_schema.dump({
            "status": 404,
            "message": "Item not found"
        }), 400

    item.checked = True
    item.save()

    return {}, 200
