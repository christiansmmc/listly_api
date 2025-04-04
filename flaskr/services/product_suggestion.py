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
    
    A estratégia de busca inclui:
    1. Busca direta para consultas curtas (≤ 3 caracteres)
    2. Busca por nome normalizado usando índice B-tree
    3. Busca fulltext do MySQL para consultas mais complexas
    
    Args:
        query_text (str): O texto de consulta para buscar sugestões
        limit (int): Número máximo de resultados a retornar
        
    Returns:
        list: Lista de objetos ProductSuggestion correspondentes à consulta
    """
    if not query_text or len(query_text.strip()) == 0:
        return []
    
    # Normaliza o texto para remover acentos
    normalized_query = normalize_text(query_text)
    
    # Cache de resultados para evitar duplicações
    result_ids = set()
    all_results = []
    
    # Estratégia 1: Busca exata pelo nome original (case insensitive)
    # Útil para buscas curtas e diretas, usa índice B-tree
    if len(query_text) <= 3:
        try:
            direct_results = ProductSuggestion.query.filter(
                func.lower(ProductSuggestion.name).startswith(query_text.lower())
            ).limit(limit).all()
            
            for result in direct_results:
                if result.id not in result_ids:
                    result_ids.add(result.id)
                    all_results.append(result)
            
            if len(all_results) >= limit:
                return all_results[:limit]
        except Exception as e:
            current_app.logger.error(f"Erro na busca direta: {str(e)}")
    
    # Estratégia 2: Busca pelo nome normalizado
    # Usa o índice btree na coluna normalized_name, muito eficiente
    try:
        normalized_results = ProductSuggestion.query.filter(
            ProductSuggestion.normalized_name.startswith(normalized_query)
        ).limit(limit).all()
        
        for result in normalized_results:
            if result.id not in result_ids:
                result_ids.add(result.id)
                all_results.append(result)
        
        if len(all_results) >= limit:
            return all_results[:limit]
    except Exception as e:
        current_app.logger.error(f"Erro na busca normalizada: {str(e)}")
    
    # Estratégia 3: Busca fulltext do MySQL para consultas mais complexas
    # Útil quando as estratégias anteriores não retornam resultados suficientes
    try:
        # Preparando os termos para busca FULLTEXT do MySQL
        # Precisamos adicionar '*' aos termos para busca de prefixo
        search_terms = ' '.join([f"{term}*" for term in normalized_query.split()])
        
        if not search_terms:
            return all_results[:limit] if all_results else []
            
        # Usando MySQL MATCH AGAINST com o operador IN BOOLEAN MODE
        sql = text("""
            SELECT id, name
            FROM product_suggestion
            WHERE MATCH(name) AGAINST(:query IN BOOLEAN MODE)
            LIMIT :limit
        """)
        
        result = db.session.execute(
            sql, 
            {"query": search_terms, "limit": limit - len(all_results)}
        )
        
        # Convertendo os resultados para objetos e evitando duplicatas
        for row in result:
            product_id = row[0]
            if product_id not in result_ids:
                product = ProductSuggestion.query.get(product_id)
                if product:
                    result_ids.add(product_id)
                    all_results.append(product)
        
    except Exception as e:
        # Log detalhado do erro
        current_app.logger.error(f"Erro na busca fulltext: {str(e)}", exc_info=True)
        
        # Fallback: busca LIKE se a busca FULLTEXT falhar
        # Isso pode acontecer se o índice FULLTEXT não estiver disponível
        try:
            like_pattern = f"%{query_text}%"
            like_results = ProductSuggestion.query.filter(
                ProductSuggestion.name.like(like_pattern)
            ).limit(limit - len(all_results)).all()
            
            for result in like_results:
                if result.id not in result_ids:
                    result_ids.add(result.id)
                    all_results.append(result)
        except Exception as e2:
            current_app.logger.error(f"Erro na busca LIKE fallback: {str(e2)}")
    
    # Retorna os resultados combinados, limitados ao número solicitado
    return all_results[:limit] if all_results else [] 