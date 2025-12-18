#!/bin/bash

# Script de teste local do Docker

echo "🐳 Testando o Docker localmente..."
echo ""

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    exit 1
fi

echo "✅ Docker encontrado"
echo ""

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Crie um arquivo .env baseado no .env.example"
    exit 1
fi

echo "✅ Arquivo .env encontrado"
echo ""

# Build da imagem
echo "🔨 Construindo imagem Docker..."
docker build -t nist-discord-bot:test .

if [ $? -eq 0 ]; then
    echo "✅ Build concluído com sucesso!"
    echo ""
else
    echo "❌ Erro no build!"
    exit 1
fi

# Perguntar se deseja executar
read -p "▶️  Deseja executar o container? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Iniciando container..."
    docker run -d --name nist-bot-test --env-file .env nist-discord-bot:test
    
    if [ $? -eq 0 ]; then
        echo "✅ Container iniciado!"
        echo ""
        echo "📊 Para ver os logs:"
        echo "   docker logs -f nist-bot-test"
        echo ""
        echo "🛑 Para parar o container:"
        echo "   docker stop nist-bot-test"
        echo ""
        echo "🗑️  Para remover o container:"
        echo "   docker rm nist-bot-test"
    else
        echo "❌ Erro ao iniciar container!"
        exit 1
    fi
fi
