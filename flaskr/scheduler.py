import logging

from flaskr.services.rooms import RoomService


def delete_inactive_rooms(app):
    logging.info('Starting to remove inactive rooms')
    with app.app_context():
        RoomService.delete_inactive_rooms()


def delete_soft_deleted_rooms(app):
    logging.info('Starting to remove soft deleted rooms')
    with app.app_context():
        RoomService.delete_soft_deleted_rooms()
