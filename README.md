# NIST Discord Bot 🛡️

Bot do Discord que monitora e notifica sobre novas CVEs (Common Vulnerabilities and Exposures) da API do NIST NVD em tempo real.

## 🚀 Características

- ✅ Monitoramento automático de novas CVEs a cada 10 minutos
- ✅ Notificações formatadas com embeds do Discord
- ✅ Sistema de persistência para evitar duplicatas
- ✅ Classificação por severidade com cores
- ✅ Suporte a CVSS v2, v3.0 e v3.1
- ✅ Links diretos para detalhes no NIST NVD
- ✅ Containerizado com Docker

## 📋 Pré-requisitos

- Python 3.11+
- Docker (para containerização)
- Token de bot do Discord
- ID do canal do Discord onde as notificações serão enviadas

## 🔧 Configuração Local

1. Clone o repositório:
```bash
git clone https://github.com/PedroNhoura/nist-discord-bot.git
cd nist-discord-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

4. Execute o bot:
```bash
python main.py
```

## 🐳 Deploy com Docker

### Build local:
```bash
docker build -t nist-discord-bot .
docker run -d --name nist-bot --env-file .env nist-discord-bot
```

### Deploy no DigitalOcean App Platform:

1. Faça push do código para o GitHub
2. No DigitalOcean, crie um novo App
3. Conecte ao repositório GitHub
4. Configure as variáveis de ambiente no painel do DigitalOcean:
   - `DISCORD_TOKEN`
   - `DISCORD_CHANNEL_ID`
   - `NVD_API_KEY` (opcional)
5. O DigitalOcean detectará automaticamente o Dockerfile e fará o deploy

## 🔐 Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DISCORD_TOKEN` | Sim | Token do bot do Discord |
| `DISCORD_CHANNEL_ID` | Sim | ID do canal para enviar notificações |
| `NVD_API_KEY` | Não | Chave API do NVD (aumenta rate limit) |

## 📊 Como Funciona

1. O bot se conecta ao Discord
2. A cada 10 minutos, consulta a API do NIST NVD
3. Busca CVEs publicadas no dia atual (UTC)
4. Compara com o último ID processado (`last_cve.txt`)
5. Envia notificações apenas de CVEs novas
6. Atualiza o arquivo de persistência

## 🎨 Classificação de Severidade

- 🔴 **CRITICAL/HIGH** - Vermelho
- 🟠 **MEDIUM** - Laranja
- 🟢 **LOW** - Verde
- 🔵 **Outros** - Azul

## 📝 Licença

Projeto desenvolvido por **Brazukas Hacking Club**

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
