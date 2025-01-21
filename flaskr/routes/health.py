from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')


@health_bp.get('')
def health():
    """
    Health Check.
    ---
    tags:
      - Health
    responses:
      200:
        description: Retorna o status da API.
        schema:
          type: object
          properties:
            status:
              type: string
              example: "ok"
    """
    return jsonify({"status": "ok"})
