import unicodedata
from sqlalchemy import func
from flaskr.models import ProductSuggestion
from flaskr.config.db import db

def normalize_text(text_input):
    """
    Remove acentos e converte para minúsculas.
    """
    if not text_input:
        return ""
    text_input = text_input.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text_input)
                   if unicodedata.category(c) != 'Mn')


def find_product_suggestions(query_text, limit=5):
    """
    Retorna sugestões de produtos que começam com o texto fornecido, 
    utilizando apenas o campo normalizado (sem acentos) para maior precisão.
    """
    if not query_text:
        return []

    normalized_query = normalize_text(query_text)

    if not normalized_query:
        return []

    results = (ProductSuggestion.query
               .filter(ProductSuggestion.normalized_name.startswith(normalized_query))
               .limit(limit)
               .all())

    return results
