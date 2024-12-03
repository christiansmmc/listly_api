from flask import Blueprint

items_bp = Blueprint('items', __name__, url_prefix='/api/v1/items')
