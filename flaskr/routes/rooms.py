from flask import Blueprint

rooms_bp = Blueprint('rooms', __name__, url_prefix='/api/v1/rooms')
