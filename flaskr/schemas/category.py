from flaskr.config.ma import ma
from flaskr.models import Item


class CategoryListResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Item
        many = True

    id = ma.auto_field()
    name = ma.auto_field()
