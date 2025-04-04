from flask import Blueprint, request, jsonify

from flaskr.schemas.product_suggestion import product_suggestions_schema
from flaskr.services.product_suggestion import find_product_suggestions

product_suggestions_bp = Blueprint('product_suggestions', __name__, url_prefix='/api/v1/product-suggestions')


@product_suggestions_bp.get('')
def get_product_suggestions():
    query_text = request.args.get('q', '')
    limit = request.args.get('limit', 5, type=int)

    if not query_text:
        return jsonify([])

    suggestions = find_product_suggestions(query_text, limit)
    return product_suggestions_schema.dump(suggestions)
