import random
from datetime import datetime

import pytz
from flask import request, abort


def get_current_time():
    return datetime.now(pytz.timezone('America/Sao_Paulo'))


def get_4_digits_code():
    random_4_digits_number = random.randint(1, 9999)
    return str(random_4_digits_number).zfill(4)


def get_room_passcode_header():
    room_passcode = request.headers.get('X-Room-Passcode')

    if not room_passcode:
        abort(401, description='Not Authorized')

    return room_passcode
