import unicodedata

from flaskr.models import ProductSuggestion


def normalize_text(text_input):
    if not text_input:
        return ""
    text_input = text_input.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text_input)
                   if unicodedata.category(c) != 'Mn')


def find_product_suggestions(query_text, limit=5):
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
