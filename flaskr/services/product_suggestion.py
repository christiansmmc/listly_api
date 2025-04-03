import unicodedata
from sqlalchemy import func, text
from flaskr.models import ProductSuggestion
from flask import current_app
from flaskr.config.db import db


def normalize_text(text_input):
    """Remove acentos e converte para minúsculas."""
    if not text_input:
        return ""
    text_input = text_input.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text_input)
                   if unicodedata.category(c) != 'Mn')


def find_product_suggestions(query_text, limit=10):
    """
    Busca sugestões de produtos que começam com o texto fornecido.
    Utiliza índices otimizados e busca de texto quando apropriado.
    """
    if not query_text or len(query_text.strip()) == 0:
        return []
    
    # Normaliza o texto para remover acentos
    normalized_query = normalize_text(query_text)
    
    # Estratégia 1: Busca exata pelo nome original (case insensitive)
    # Útil para buscas curtas e diretas, usa índice B-tree
    if len(query_text) <= 3:
        direct_results = ProductSuggestion.query.filter(
            func.lower(ProductSuggestion.name).startswith(query_text.lower())
        ).limit(limit).all()
        
        if direct_results:
            return direct_results
    
    # Estratégia 2: Busca pelo nome normalizado
    # Usa o índice btree na coluna normalized_name, muito eficiente
    normalized_results = ProductSuggestion.query.filter(
        ProductSuggestion.normalized_name.startswith(normalized_query)
    ).limit(limit).all()
    
    if normalized_results:
        return normalized_results
    
    # Estratégia 3: Busca full-text para consultas mais complexas ou sem correspondência exata
    # Usa o índice GIN para busca de texto completo (mais flexível, mas pode ser mais lento)
    try:
        # Preparando o padrão de consulta para ts_query
        ts_query = ' & '.join(normalized_query.split()) + ':*'
        
        # Usando consulta SQL direta para aproveitar o ts_query
        sql = text("""
            SELECT id, name
            FROM product_suggestion
            WHERE to_tsvector('portuguese', immutable_unaccent(name)) @@ to_tsquery('portuguese', :query)
            ORDER BY ts_rank(to_tsvector('portuguese', immutable_unaccent(name)), to_tsquery('portuguese', :query)) DESC
            LIMIT :limit
        """)
        
        result = db.session.execute(
            sql, 
            {"query": ts_query, "limit": limit}
        )
        
        # Convertendo os resultados para objetos
        fulltext_results = [
            ProductSuggestion.query.get(row[0])
            for row in result
        ]
        
        if fulltext_results:
            return fulltext_results
            
    except Exception as e:
        # Log do erro mas continua com outras estratégias
        current_app.logger.error(f"Erro na busca full-text: {str(e)}")
    
    # Se nenhuma estratégia retornou resultados, retorna lista vazia
    return [] 