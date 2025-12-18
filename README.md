# NIST Discord Bot 🛡️

Bot do Discord que monitora e notifica sobre novas CVEs (Common Vulnerabilities and Exposures) da API do NIST NVD em tempo real.

## 🚀 Características

- ✅ Monitoramento automático de novas CVEs a cada 10 minutos
- ✅ Notificações formatadas com embeds do Discord
- ✅ Sistema de persistência para evitar duplicatas
- ✅ Classificação por severidade com cores (Critical, High, Medium, Low)
- ✅ Suporte a CVSS v2, v3.0 e v3.1
- ✅ Links diretos para detalhes no NIST NVD
- ✅ Containerizado com Docker
- ✅ Health check HTTP para monitoramento
- ✅ Deploy fácil no DigitalOcean App Platform

## 📋 Pré-requisitos

- Token de bot do Discord ([criar aqui](https://discord.com/developers/applications))
- ID do canal do Discord para notificações
- Docker (opcional, para testes locais)
- Conta DigitalOcean (para deploy em produção)

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
DISCORD_TOKEN=seu_token_aqui
DISCORD_CHANNEL_ID=seu_channel_id_aqui
NVD_API_KEY=sua_chave_opcional  # Recomendado para evitar rate limits
PORT=8080  # Porta para health check (padrão: 8080)
```

### Obter Credenciais

**Discord Token:**
1. Acesse https://discord.com/developers/applications
2. Crie um novo Application
3. Vá em "Bot" → "Add Bot"
4. Copie o Token
5. Em OAuth2 → URL Generator: marque `bot` e permissões necessárias
6. Adicione o bot ao seu servidor

**Channel ID:**
1. Ative o Modo Desenvolvedor no Discord (Configurações → Avançado)
2. Clique com botão direito no canal → Copiar ID

**NVD API Key (Opcional):**
1. Acesse https://nvd.nist.gov/developers/request-an-api-key
2. Preencha o formulário
3. Receba a chave por email
4. Aumenta rate limit de 5 para 50 requisições/30s

## � Deploy

### Opção 1: DigitalOcean App Platform (Recomendado)

**Passos:**

1. **Criar App**
   - Acesse: https://cloud.digitalocean.com/apps
   - Clique em "Create App"
   - Conecte ao GitHub e selecione este repositório
   - Branch: `main`

2. **Escolher Build Method**
   - Quando detectar, selecione: **Dockerfile** (não Buildpack)
   - Resource Type: **Web Service**
   - Instance Size: `apps-s-1vcpu-1gb-fixed` ($10/mês)

3. **Configurar Environment Variables**
   ```
   DISCORD_TOKEN = [seu_token] (Secret)
   DISCORD_CHANNEL_ID = [seu_channel_id]
   NVD_API_KEY = [sua_chave] (Secret, opcional)
   ```

4. **Configurações Finais**
   - HTTP Port: `8080` (já configurado)
   - Region: Escolha o mais próximo (ex: ATL1)
   - Auto-deploy: Habilitado

5. **Deploy**
   - Clique em "Create Resources"
   - Aguarde 2-3 minutos

**Custo:** $10/mês | **Uptime:** 99.99% | **Auto-scaling:** Disponível

### Opção 2: Docker Local (Testes)

```bash
# Build
docker build -t nist-discord-bot .

# Run
docker run -d --name nist-bot --env-file .env nist-discord-bot

# Logs
docker logs -f nist-bot

# Stop
docker stop nist-bot && docker rm nist-bot
```

### Opção 3: Docker Compose

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Opção 4: Python Direto

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## � Arquitetura

```
┌─────────────────────────────────────────┐
│   Discord Bot (Python 3.11)             │
│   ┌─────────────────────────────────┐   │
│   │  HTTP Server (port 8080)        │   │  ← Health Check
│   │  /health  /                     │   │
│   └─────────────────────────────────┘   │
│   ┌─────────────────────────────────┐   │
│   │  CVE Monitor (10min interval)   │   │
│   │  - Fetch NVD API                │   │
│   │  - Check new CVEs               │   │
│   │  - Send to Discord              │   │
│   └─────────────────────────────────┘   │
│   ┌─────────────────────────────────┐   │
│   │  Persistence (last_cve.txt)     │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
          │                    │
          ▼                    ▼
    Discord API          NIST NVD API
```

## 📊 Como Funciona

1. O bot se conecta ao Discord
2. Inicia um servidor HTTP na porta 8080 para health checks (DigitalOcean)
3. A cada 10 minutos, consulta a API do NIST NVD
4. Busca CVEs publicadas no dia atual (UTC)
5. Compara com o último ID processado (`last_cve.txt`)
6. Envia notificações apenas de CVEs novas
7. Atualiza o arquivo de persistência

## 🎨 Classificação de Severidade

- 🔴 **CRITICAL/HIGH** - Vermelho
- 🟠 **MEDIUM** - Laranja
- 🟢 **LOW** - Verde
- 🔵 **Outros** - Azul

## �️ Troubleshooting

### Bot não conecta ao Discord
- Verifique se o token está correto
- Confirme que o bot foi adicionado ao servidor
- Veja logs para erros de autenticação

### Não recebe notificações
- Verifique se o CHANNEL_ID está correto
- Confirme que o bot tem permissão para enviar mensagens no canal
- Aguarde até 10 minutos para a próxima verificação

### "Readiness probe failed"
- Aguarde 1-2 minutos para o bot inicializar completamente
- Verifique se a porta 8080 está configurada
- Veja os runtime logs no DigitalOcean

### Rate limit na API NVD
- Configure a variável `NVD_API_KEY`
- Sem chave: 5 requisições/30s
- Com chave: 50 requisições/30s

## 📈 Monitoramento

### Health Check
```bash
curl https://seu-app.ondigitalocean.app/health
# Retorna: OK
```

### Métricas
- CPU: < 5% em idle, < 20% durante verificação
- RAM: ~150-200 MB
- Network: Mínimo (apenas APIs)

## 🔐 Segurança

- ✅ Nunca commite o arquivo `.env`
- ✅ Use variáveis de ambiente para secrets
- ✅ Configure tokens como "Secret" no DigitalOcean
- ✅ Rotacione tokens periodicamente
- ✅ Mantenha dependências atualizadas

## 📄 Estrutura do Projeto

```
nist-discord-bot/
├── main.py                 # Código principal do bot
├── requirements.txt        # Dependências Python
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── Procfile              # Process definition
├── .python-version       # Python version spec
├── .dockerignore         # Docker build exclusions
├── .gitignore           # Git exclusions
├── .env.example         # Template de variáveis
└── README.md           # Esta documentação
```

## 🤝 Contribuições

Contribuições são bem-vindas! 

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Projeto desenvolvido por **Brazukas Hacking Club** 🛡️

## 🔗 Links Úteis

- [Discord Developer Portal](https://discord.com/developers/applications)
- [NIST NVD API](https://nvd.nist.gov/developers)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
- [Docker Documentation](https://docs.docker.com/)

---

**Versão:** 2.0 | **Python:** 3.11 | **Status:** ✅ Production Ready
