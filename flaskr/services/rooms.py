import logging
from datetime import timedelta

from flaskr.models import Room
from flaskr.schemas.error import ErrorSchema
from flaskr.utils import get_current_time, get_4_digits_code


class RoomService:
    @staticmethod
    def delete_inactive_rooms():
        inactive_rooms = Room.query.filter_by(active=False, deleted_at=None).all()
        for inactive_room in inactive_rooms:
            inactive_room.delete()

        logging.info(f'{len(inactive_rooms)} inactive rooms deleted')

    @staticmethod
    def delete_soft_deleted_rooms():
        SOFT_DELETE_THRESHOLD = get_current_time() - timedelta(hours=24)

        soft_delete_rooms = Room.query.filter(
            Room.deleted_at.isnot(None),
            Room.deleted_at < SOFT_DELETE_THRESHOLD
        ).all()

        for room in soft_delete_rooms:
            room.delete()

        logging.info(f'{len(soft_delete_rooms)} soft deleted rooms deleted')

    @staticmethod
    def generate_unique_room_code():
        while True:
            code = get_4_digits_code()
            if not Room.query.filter_by(code=code).first():
                return code

    @staticmethod
    def find_room_by_code(code, passcode):
        room = Room.query.filter_by(code=code, passcode=passcode, active=True).first()

        if not room:
            error_schema = ErrorSchema()
            return error_schema.dump({
                "status": 404,
                "message": "Room not found"
            }), 400

        if not room.active or room.deleted_at is not None:
            error_schema = ErrorSchema()
            return error_schema.dump({
                "status": 400,
                "message": "Room is not active"
            }), 400

        return room
