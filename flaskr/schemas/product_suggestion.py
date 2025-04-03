from flaskr.config.ma import ma
from flaskr.models import ProductSuggestion


class ProductSuggestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductSuggestion
        fields = ('name',)


product_suggestion_schema = ProductSuggestionSchema()
product_suggestions_schema = ProductSuggestionSchema(many=True) 