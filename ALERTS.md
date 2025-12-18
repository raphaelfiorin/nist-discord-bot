# 🚨 Guia de Alertas e Monitoramento

## Sistema de Alertas Implementado no Bot

### ✅ Alertas Automáticos (Já Incluídos)

O bot agora envia alertas automáticos para o Discord:

#### 1. **Alerta de Inicialização** 🟢
Quando o bot inicia com sucesso:
```
🟢 Bot Online
Status: ✅ Operacional
Monitoramento: Ativo (10 min)
```

#### 2. **Alerta de Erros Consecutivos** ⚠️
Após 3 erros seguidos ao buscar CVEs:
```
⚠️ Alerta: Erros Consecutivos
O bot encontrou 3 erros consecutivos ao buscar CVEs.
Última verificação bem-sucedida: [timestamp]
Erros consecutivos: 3
```

#### 3. **Alerta Crítico de Inatividade** 🔴
Se passar 20 minutos sem conseguir verificar CVEs:
```
🔴 Alerta Crítico: Sistema Inativo
O bot não consegue verificar CVEs há X minutos.
Última verificação bem-sucedida: [timestamp]
```

---

## 🔍 Health Check Aprimorado

### Endpoint `/health`
```bash
curl https://seu-app.ondigitalocean.app/health
```

**Respostas:**
- `200 OK` - Bot saudável (< 20 min desde última verificação)
- `503 UNHEALTHY` - Bot com problemas (> 20 min sem verificar)

### Endpoint `/` (Status Detalhado)
```bash
curl https://seu-app.ondigitalocean.app/
```

**Retorna:**
```
NIST Discord Bot - Brazukas Hacking Club
Status: 🟢 Healthy
Last Check: 2025-12-18 22:30:15 UTC
Errors: 0
Bot User: NIST#0073
```

---

## 📊 DigitalOcean Resource Alerts

### Opção 1: Email Alerts (Nativo)

**Configure no painel DigitalOcean:**

1. Apps → Seu App → Settings → Alerts
2. Create Alert:
   - **Metric**: CPU Utilization / Memory Utilization
   - **Threshold**: 
     - CPU > 80% (alerta se sobrecarga)
     - Memory > 85% (alerta se memória cheia)
   - **Notification**: Email (`crixuspedro@gmail.com`)
   - **Name**: "Bot Resource Alert"

**Limitações:**
- ❌ Não envia para Discord diretamente
- ✅ Envia para email
- ⚠️ Requer verificação de email

---

### Opção 2: Slack → Discord Bridge

DigitalOcean suporta Slack. Você pode criar uma ponte:

#### **Passo 1: Criar Webhook Discord**
1. Discord → Server Settings → Integrations → Webhooks
2. New Webhook
3. Escolha o canal
4. Copie a URL: `https://discord.com/api/webhooks/[ID]/[TOKEN]`

#### **Passo 2: Criar Workspace Slack** (Grátis)
1. Acesse: https://slack.com/create
2. Crie um workspace (ex: "bot-alerts")
3. Crie um canal (ex: #digitalocean-alerts)

#### **Passo 3: Integração Slack → Discord**
Use um serviço como:
- **Zapier** (grátis até 100 ações/mês)
- **Integromat/Make** (grátis até 1000 ops/mês)
- **n8n** (self-hosted, grátis)

**Fluxo:**
```
DigitalOcean Alert → Slack → Zapier → Discord Webhook
```

**Zapier Setup:**
1. Trigger: New Message in Slack
2. Action: Send Discord Webhook
3. Map: Slack message → Discord embed

---

### Opção 3: Monitoramento Externo (UptimeRobot)

**UptimeRobot** (Grátis) + Discord Webhook

#### **Setup:**

1. **Criar Conta**: https://uptimerobot.com
2. **Add Monitor**:
   - Type: HTTP(s)
   - URL: `https://seu-app.ondigitalocean.app/health`
   - Interval: 5 minutes
3. **Alert Contacts**:
   - Type: Webhook
   - URL: Seu Discord Webhook
   - POST Data:
     ```json
     {
       "content": "🔴 **Bot Down** - *monitorName* está offline!",
       "embeds": [{
         "title": "Alerta de Downtime",
         "description": "*alertDetails*",
         "color": 15158332
       }]
     }
     ```

**Vantagens:**
- ✅ Gratuito
- ✅ Monitora de fora (independente)
- ✅ Envia direto para Discord
- ✅ Fácil de configurar

---

## 🎯 Recomendação de Configuração Completa

### **Alertas em 3 Camadas:**

#### **Camada 1: Bot Auto-Monitoramento** ⭐ (JÁ IMPLEMENTADO)
- ✅ Alertas em tempo real no Discord
- ✅ Detecta erros consecutivos
- ✅ Alerta de inatividade
- ✅ Status de inicialização

#### **Camada 2: UptimeRobot** (RECOMENDADO)
- ✅ Monitora de fora
- ✅ Webhook direto para Discord
- ✅ Gratuito
- ⏱️ **Setup:** 5 minutos

#### **Camada 3: DigitalOcean Email Alerts** (OPCIONAL)
- ⚠️ Apenas para alertas de recursos (CPU/RAM)
- 📧 Via email
- ⏱️ **Setup:** 2 minutos

---

## 📝 Configuração Passo a Passo - UptimeRobot + Discord

### 1. Criar Discord Webhook

No Discord:
1. Server Settings → Integrations → Webhooks
2. New Webhook
3. Nome: "UptimeRobot Alerts"
4. Canal: Mesmo do bot (#cve-alerts ou similar)
5. Copiar URL do webhook

### 2. Configurar UptimeRobot

1. **Criar conta**: https://uptimerobot.com/signUp
2. **Add New Monitor**:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: NIST Bot Health
   URL: https://seu-app.ondigitalocean.app/health
   Monitoring Interval: Every 5 minutes
   ```

3. **Add Alert Contact**:
   ```
   Alert Contact Type: Webhook
   Friendly Name: Discord Alert
   URL to Notify: [Cole seu Discord Webhook]
   POST Value (JSON Format):
   ```

   ```json
   {
     "content": "@everyone 🔴 **NIST Bot está OFFLINE!**",
     "embeds": [{
       "title": "⚠️ Alerta de Downtime",
       "description": "O bot NIST CVE Monitor não está respondendo.",
       "color": 15158332,
       "fields": [
         {
           "name": "Status",
           "value": "*alertDetails*",
           "inline": false
         },
         {
           "name": "URL",
           "value": "*monitorURL*",
           "inline": false
         }
       ],
       "timestamp": "*alertDateTime*",
       "footer": {
         "text": "UptimeRobot Monitor"
       }
     }]
   }
   ```

4. **Ativar Monitor** e **Salvar**

### 3. Testar

No UptimeRobot:
- Clique no monitor
- "Advanced" → "Pause Monitoring"
- Aguarde 5 minutos
- Você receberá um alerta no Discord!
- "Resume Monitoring"

---

## 📱 Exemplo de Alerta no Discord

```
@everyone 🔴 NIST Bot está OFFLINE!

⚠️ Alerta de Downtime
O bot NIST CVE Monitor não está respondendo.

Status: Down
URL: https://seu-app.ondigitalocean.app/health
Timestamp: 2025-12-18 22:45:00 UTC

UptimeRobot Monitor
```

---

## 🔧 Troubleshooting

### UptimeRobot não envia para Discord
- ✅ Verifique se o webhook Discord está correto
- ✅ Teste o webhook manualmente com curl
- ✅ Verifique se o formato JSON está correto

### Bot não envia alertas internos
- ✅ Verifique se o CHANNEL_ID está correto
- ✅ Confirme que o bot tem permissões no canal
- ✅ Veja os logs no DigitalOcean

### Health check retorna 503
- ⚠️ Bot está com problemas há mais de 20 minutos
- ✅ Veja os runtime logs
- ✅ Verifique se as APIs (Discord/NVD) estão acessíveis

---

## 💰 Custos

| Solução | Custo | Limitações |
|---------|-------|------------|
| **Bot Auto-Monitoramento** | Grátis | Só funciona se bot estiver online |
| **UptimeRobot** | Grátis | 50 monitores, intervalo 5 min |
| **UptimeRobot Pro** | $7/mês | Intervalo 1 min, SMS alerts |
| **Zapier** | Grátis | 100 ações/mês |
| **DigitalOcean Alerts** | Grátis | Apenas email/Slack |

---

## ✅ Checklist de Implementação

- [x] Bot auto-monitoramento implementado
- [x] Health check aprimorado
- [ ] Criar Discord Webhook para alertas
- [ ] Configurar UptimeRobot
- [ ] Configurar DigitalOcean Email Alerts
- [ ] Testar todos os alertas

---

**Recomendação Final**: Use **Bot Auto-Monitoramento** + **UptimeRobot** para cobertura completa! 🎯
