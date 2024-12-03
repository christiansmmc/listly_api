from flask import Blueprint

health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')


@health_bp.get('')
def health():
    return {"status": "ok"}
