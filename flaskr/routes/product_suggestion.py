from flask import Blueprint, request, jsonify
from flasgger import swag_from

from flaskr.services.product_suggestion import find_product_suggestions
from flaskr.schemas.product_suggestion import product_suggestions_schema

product_suggestions_bp = Blueprint('product_suggestions', __name__, url_prefix='/product-suggestions')


@product_suggestions_bp.route('', methods=['GET'])
def get_product_suggestions():
    """Retorna sugestões de produtos baseado no texto de busca."""
    query_text = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query_text:
        return jsonify([])
    
    suggestions = find_product_suggestions(query_text, limit)
    return jsonify(product_suggestions_schema.dump(suggestions)) 