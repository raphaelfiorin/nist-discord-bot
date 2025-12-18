# 🚀 Guia de Deploy - DigitalOcean App Platform

## Configuração no DigitalOcean

### 1️⃣ Preparação do Repositório GitHub

Certifique-se de que todos os arquivos estão commitados e enviados:

```bash
git add .
git commit -m "Add Docker configuration for DigitalOcean"
git push origin main
```

### 2️⃣ Criação do App no DigitalOcean

1. Acesse o [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Clique em **"Create App"**
3. Selecione **GitHub** como source provider
4. Escolha o repositório: `PedroNhoura/nist-discord-bot`
5. Selecione a branch: `main`
6. Mantenha **Auto-deploy on push** habilitado

### 3️⃣ Configuração do Resource

**Configurações Importantes:**

- **Name**: `nist-discord-bot`
- **Resource Type**: Web Service
- **Instance Size**: apps-s-1vcpu-1gb-fixed ($10/mo)
- **Build Strategy**: Dockerfile (será detectado automaticamente)
- **HTTP Port**: 8080
- **Region**: ATL1 (Atlanta) ou o mais próximo dos usuários

### 4️⃣ Variáveis de Ambiente ⚠️ CRÍTICO

No painel do DigitalOcean, adicione estas variáveis de ambiente:

| Key | Value | Observação |
|-----|-------|------------|
| `DISCORD_TOKEN` | `seu_token_aqui` | ⚠️ Obrigatório |
| `DISCORD_CHANNEL_ID` | `seu_channel_id` | ⚠️ Obrigatório |
| `NVD_API_KEY` | `sua_chave_aqui` | Opcional (recomendado) |

**IMPORTANTE**: 
- ❌ NÃO commite o arquivo `.env` no GitHub
- ✅ Configure as variáveis direto no painel do DigitalOcean
- ✅ Use o arquivo `.env.example` como referência

### 5️⃣ App Name e Projeto

- **App Name**: `starfish-app` (ou outro nome único em lowercase)
- **Project**: `Bot_Brazukas_HC`
- **Environment**: Production

### 6️⃣ Custos

- **Resource**: $10.00/mês
- **Total**: $10.00/mês

## 🔍 Verificação Pós-Deploy

Após o deploy, verifique:

1. **Build Logs**: Verifique se o build do Docker foi bem-sucedido
2. **Runtime Logs**: Confirme que o bot conectou ao Discord
   - Procure por: `Bot conectado como [nome] (ID: xxx)`
   - Procure por: `Tarefa de monitoramento de CVEs iniciada.`
3. **Health Status**: Deve mostrar "Healthy" (verde)

## 🐛 Troubleshooting

### Bot não conecta ao Discord
- ✅ Verifique se `DISCORD_TOKEN` está correto nas env vars
- ✅ Verifique se o token não expirou
- ✅ Confirme que o bot está adicionado ao servidor

### Não recebe notificações
- ✅ Verifique se `DISCORD_CHANNEL_ID` está correto
- ✅ Confirme que o bot tem permissões para enviar mensagens
- ✅ Verifique os logs de runtime

### Build falha
- ✅ Verifique se o Dockerfile está no root do repositório
- ✅ Confirme que `requirements.txt` está presente
- ✅ Veja os build logs para detalhes

## 📊 Monitoramento

### Logs em Tempo Real
```bash
# Via CLI do DigitalOcean
doctl apps logs <app-id> --type RUN --follow
```

### Métricas Importantes
- **CPU Usage**: Deve ficar baixo (< 20%) na maioria do tempo
- **Memory Usage**: Deve ficar abaixo de 500MB
- **Restart Count**: Deve ser zero ou muito baixo

## 🔄 Atualizações

Para atualizar o bot:

1. Faça as alterações no código localmente
2. Commit e push para o GitHub:
```bash
git add .
git commit -m "Descrição da alteração"
git push origin main
```
3. O DigitalOcean fará o deploy automático (Auto-deploy está habilitado)

## 🔐 Segurança

### Boas Práticas:
- ✅ Nunca commite credenciais no código
- ✅ Use variáveis de ambiente para todos os secrets
- ✅ Mantenha o `.env` no `.gitignore`
- ✅ Rotacione tokens periodicamente
- ✅ Use `NVD_API_KEY` para evitar rate limits

## 📱 Permissões do Bot Discord

Certifique-se de que o bot tem estas permissões:

- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Message History
- ✅ View Channel

## 🎯 Próximos Passos (Opcional)

Após o deploy básico funcionar:

1. **Custom Domain**: Configure um domínio personalizado
2. **Alertas**: Configure alertas de uptime
3. **Backup**: Configure backup automático do `last_cve.txt`
4. **Escalabilidade**: Considere aumentar a instância se necessário
5. **Logging**: Configure log forwarding para análise

## 📞 Suporte

Em caso de problemas:
- Logs do DigitalOcean: Menu lateral > Runtime Logs
- Discord API Status: https://discordstatus.com/
- NVD API Status: https://nvd.nist.gov/

---

**Desenvolvido por Brazukas Hacking Club** 🛡️
