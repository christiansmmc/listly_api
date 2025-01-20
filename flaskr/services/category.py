from flask import abort

from flaskr.models import Category


class CategoryService:
    @staticmethod
    def get_category_or_default(category_id, default_name='Outros'):
        if category_id:
            category = Category.query.get(category_id)
        else:
            category = Category.query.filter_by(name=default_name).first()

        if not category:
            abort(404, description='Category not found')

        return category
