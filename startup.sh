#!/bin/bash

# Configuração de variáveis de ambiente
export PYTHONPATH=/app:$PYTHONPATH

# Cria os diretórios necessários
# echo "Configurando diretórios..."
# python -c "from util.setup_dirs import setup_directories; setup_directories()"

# Pré-carrega os modelos do rembg (com timeout para não travar o processo)
echo "Pré-carregando modelos (timeout 60s)..."
timeout 3 python -m util.preload_models || echo "Aviso: Pré-carregamento de modelos falhou, mas continuando a inicialização"

# Inicia o Gunicorn com configurações otimizadas
echo "Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 \
              --workers 1 \
              --threads 4 \
              --timeout 120 \
              --log-level info \
              wsgi:app
