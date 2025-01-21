from flask import Blueprint

from flaskr.models import Category
from flaskr.schemas.category import CategoryListResponseSchema

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.get('')
def get_categories():
    categories = Category.query.all()

    category_scheam = CategoryListResponseSchema()
    return category_scheam.dump(categories), 200
