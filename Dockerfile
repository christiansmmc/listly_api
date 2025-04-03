FROM python:3.9-slim

# Evita .pyc e ativa logs direto no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Porta da aplicação
EXPOSE 5000
