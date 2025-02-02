from flask import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from flaskr.models import Item
from flaskr.schemas.item import ItemCreateRequestSchema
from flaskr.schemas.validation import validate_schema
from flaskr.services.category import CategoryService
from flaskr.services.rooms import RoomService
from flaskr.utils import validate_jwt_room_code

rooms_items_bp = Blueprint('items', __name__, url_prefix='/api/v1/rooms/<string:room_code>/items')


@rooms_items_bp.post('')
@jwt_required()
def add_item(room_code):
    jwt_room_code = get_jwt_identity()
    validate_jwt_room_code(jwt_room_code, room_code, 404, "Room not found")

    request_body = validate_schema(ItemCreateRequestSchema)

    room = RoomService.find_room_by_code(jwt_room_code)
    item = Item(name=request_body['name'], room_id=room.id)

    category = CategoryService.get_category_or_default(request_body.get('category_id'))

    item.category = category
    item.save()

    return {'id': item.id}, 201


@rooms_items_bp.delete('/<int:item_id>')
@jwt_required()
def delete_item(room_code, item_id):
    jwt_room_code = get_jwt_identity()
    validate_jwt_room_code(jwt_room_code, room_code, 404, "Room not found")

    room = RoomService.find_room_by_code(jwt_room_code)
    item = Item.query.filter_by(room_id=room.id, id=item_id).first()

    if not item:
        return {}, 204

    item.delete()

    return {}, 204


@rooms_items_bp.patch('/<int:item_id>')
@jwt_required()
def check_item(room_code, item_id):
    jwt_room_code = get_jwt_identity()
    validate_jwt_room_code(jwt_room_code, room_code, 404, "Room not found")

    room = RoomService.find_room_by_code(room_code)
    item = Item.query.filter_by(room_id=room.id, id=item_id).first()

    if not item:
        abort(404, description="Item not found")

    item.checked = not item.checked
    item.save()

    return {}, 200
