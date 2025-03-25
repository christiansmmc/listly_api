import logging
from datetime import timedelta

from flask import abort

from flaskr.models import Room, RoomAccess
from flaskr.utils import get_current_time, get_4_digits_code
from werkzeug.security import check_password_hash


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
    def find_room_by_code(code):
        room = Room.query.filter_by(code=code, active=True).first()

        if not room:
            abort(404, "Room not found")

        if not room.active or room.deleted_at is not None:
            abort(400, "Room is not active")

        return room

    @staticmethod
    def validate_room(code, passcode):
        room = Room.query.filter_by(code=code, active=True).first()
        
        if not room:
            abort(404, "Room not found")
        
        if not room.active or room.deleted_at is not None:
            abort(400, "Room is not active")
        
        if not check_password_hash(room.passcode, passcode):
            abort(401, description='Invalid passcode')
        
        return room

    @staticmethod
    def validate_room_access_code(code, access_code):
        room_access = RoomAccess.query.join(Room).filter(
            Room.code == code,
            RoomAccess.access_code == access_code,
            RoomAccess.expiration_date > get_current_time(),
            Room.active == True,
            Room.deleted_at.is_(None)
        ).first()

        if not room_access:
            abort(404, "Room access not found or expired")

        return room_access.room
