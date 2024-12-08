from flask import Blueprint

from flaskr.models import Item, Room
from flaskr.schemas.error import ErrorSchema
from flaskr.schemas.item import ItemCreateRequestSchema
from flaskr.schemas.validation import validate_schema
from flaskr.services.rooms import RoomService
from flaskr.utils import get_room_passcode_header

rooms_items_bp = Blueprint('items', __name__, url_prefix='/api/v1/rooms/<string:room_code>/items')


@rooms_items_bp.post('/items')
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


@rooms_items_bp.delete('/<int:item_id>')
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


@rooms_items_bp.patch('/items/<int:item_id>')
def check_item(room_code, item_id):
    room_passcode = get_room_passcode_header()
    if isinstance(room_passcode, tuple):
        return room_passcode

    room = RoomService.find_room_by_code(room_code, room_passcode)
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
