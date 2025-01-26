from flask import Blueprint, abort

from flaskr.models import Item, Room
from flaskr.schemas.item import ItemCreateRequestSchema
from flaskr.schemas.validation import validate_schema
from flaskr.services.category import CategoryService
from flaskr.services.rooms import RoomService
from flaskr.utils import get_room_passcode_header

rooms_items_bp = Blueprint('items', __name__, url_prefix='/api/v1/rooms/<string:room_code>/items')


@rooms_items_bp.post('')
def add_item(room_code):
    room_passcode = get_room_passcode_header()

    request_body = validate_schema(ItemCreateRequestSchema)

    room = RoomService.find_room_by_code(room_code, room_passcode)
    item = Item(name=request_body['name'], room_id=room.id)

    category = CategoryService.get_category_or_default(request_body.get('category_id'))

    item.category = category
    item.save()

    return {'id': item.id}, 201


@rooms_items_bp.delete('/<int:item_id>')
def delete_item(room_code, item_id):
    room_passcode = get_room_passcode_header()

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


@rooms_items_bp.patch('/<int:item_id>')
def check_item(room_code, item_id):
    room_passcode = get_room_passcode_header()

    room = RoomService.find_room_by_code(room_code, room_passcode)
    item = Item.query.filter_by(room_id=room.id, id=item_id).first()

    if not item:
        abort(404, description="Item not found")

    item.checked = not item.checked
    item.save()

    return {}, 200
