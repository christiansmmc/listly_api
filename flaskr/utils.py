import random
from datetime import datetime

import pytz
from flask import request, abort


def get_current_time():
    return datetime.now(pytz.timezone('America/Sao_Paulo'))


def get_4_digits_code():
    random_4_digits_number = random.randint(1, 9999)
    return str(random_4_digits_number).zfill(4)

def validate_jwt_room_code(jwt_room_code, url_room_code, error_code, error_message):
    if jwt_room_code != url_room_code:
        abort(error_code, error_message)
