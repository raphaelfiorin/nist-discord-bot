# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro (melhor para cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container
COPY . .

# Cria o arquivo de persistência se não existir
RUN touch last_cve.txt

# Expõe a porta 8080 (mesmo que não seja usado, o DigitalOcean espera isso)
EXPOSE 8080

# Define variáveis de ambiente padrão (serão sobrescritas pelas do DigitalOcean)
ENV PYTHONUNBUFFERED=1

# Comando para executar o bot
CMD ["python", "-u", "main.py"]
