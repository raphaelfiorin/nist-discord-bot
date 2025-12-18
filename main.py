import discord
import asyncio
import requests
import os
import logging
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
NVD_API_KEY = os.getenv('NVD_API_KEY')

# Arquivo para persistência do último ID
LAST_CVE_FILE = 'last_cve.txt'
# Endpoint base da API do NVD
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0/"

# Verificar configurações obrigatórias
if not TOKEN or not CHANNEL_ID:
    logger.error("ERRO: DISCORD_TOKEN ou DISCORD_CHANNEL_ID não configurados no arquivo .env")
    exit(1)

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    logger.error("ERRO: DISCORD_CHANNEL_ID deve ser um número inteiro.")
    exit(1)

class CVEBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = None

    async def on_ready(self):
        logger.info(f'Bot conectado como {self.user} (ID: {self.user.id})')
        # Inicia a tarefa de monitoramento se ainda não estiver rodando
        if self.bg_task is None:
            self.bg_task = self.loop.create_task(self.monitor_cves_task())
            logger.info("Tarefa de monitoramento de CVEs iniciada.")

    async def monitor_cves_task(self):
        """Loop principal de monitoramento."""
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        
        if not channel:
            logger.error(f"Não foi possível encontrar o canal com ID {CHANNEL_ID}. Verifique as permissões e o ID.")
            return

        while not self.is_closed():
            try:
                logger.info("Verificando novas CVEs...")
                new_cves = await self.fetch_and_process_cves()
                
                if new_cves:
                    logger.info(f"Encontradas {len(new_cves)} novas CVEs. Enviando...")
                    for i, cve in enumerate(new_cves):
                        try:
                            cve_id = cve['cve']['id']
                            logger.info(f"Enviando {i+1}/{len(new_cves)}: {cve_id}")
                            
                            embed = self.create_cve_embed(cve)
                            await channel.send(embed=embed)
                            
                            # Atualiza o arquivo a cada envio para garantir persistência
                            self.save_last_cve_id(cve_id)
                            
                            # Pequena pausa para evitar rate limit do Discord
                            await asyncio.sleep(2)
                        except Exception as e_send:
                            logger.error(f"Erro ao enviar CVE {cve.get('cve', {}).get('id', 'unknown')}: {e_send}")
                            # Continua para o próximo item mesmo se este falhar
                            continue
                else:
                    logger.info("Nenhuma nova CVE encontrada neste ciclo.")

            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
            
            # Aguarda 10 minutos antes da próxima verificação
            await asyncio.sleep(600)

    async def fetch_and_process_cves(self):
        """Busca CVEs na API e filtra as novas."""
        # Definir datas para o dia atual (UTC)
        now = datetime.now(timezone.utc)
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999)
        
        # Formato exigido pela NVD API
        fmt = '%Y-%m-%dT%H:%M:%S.%f'
        pub_start = start_date.strftime(fmt)[:-3]
        pub_end = end_date.strftime(fmt)[:-3]

        params = {
            'pubStartDate': pub_start,
            'pubEndDate': pub_end,
            'resultsPerPage': 2000  # Tenta pegar todas do dia em uma requisição
        }
        
        headers = {}
        if NVD_API_KEY:
            headers['apiKey'] = NVD_API_KEY

        try:
            # Executa requests em um executor para não bloquear o loop asyncio
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(NVD_API_URL, params=params, headers=headers, timeout=30)
            )
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data.get('vulnerabilities', [])
                
                if not vulnerabilities:
                    return []

                # Ordenar por data de publicação (da mais antiga para a mais recente)
                # Isso garante que enviemos na ordem correta e atualizemos o "último visto" progressivamente
                vulnerabilities.sort(key=lambda x: x['cve']['published'])

                last_id = self.get_last_cve_id()
                new_items = []
                
                if last_id:
                    # Se temos um último ID, precisamos encontrar onde ele está na lista
                    # e pegar tudo que vem DEPOIS dele.
                    start_index = -1
                    for i, item in enumerate(vulnerabilities):
                        if item['cve']['id'] == last_id:
                            start_index = i
                            break
                    
                    if start_index != -1:
                        # Pega todos os itens APÓS o último visto
                        new_items = vulnerabilities[start_index + 1:]
                    else:
                        # Se o ID salvo não está na lista de hoje:
                        # Pode ser que o ID salvo seja de ontem. Nesse caso, TODOS de hoje são novos.
                        # Para evitar duplicatas caso o ID esteja apenas em outra página (improvável com 2000 limite),
                        # assumimos que se não achou e a data mudou, envia tudo.
                        # Mas como filtramos a API por "hoje", se o last_id não está aqui, ele é antigo.
                        new_items = vulnerabilities
                else:
                    # Se não tem arquivo (primeira execução), para evitar spam,
                    # enviamos apenas a última CVE (a mais recente) encontrada hoje.
                    # Isso serve como confirmação de funcionamento e marca o ponto de partida.
                    if vulnerabilities:
                        new_items = [vulnerabilities[-1]]
                    else:
                        new_items = []

                return new_items
            
            elif response.status_code == 403 or response.status_code == 429:
                logger.warning("Rate limit atingido ou acesso negado. Aguardando...")
                await asyncio.sleep(60) # Espera extra se der rate limit
                return []
            else:
                logger.error(f"Erro na API NVD: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Exceção ao buscar CVEs: {e}")
            return []

    def get_last_cve_id(self):
        """Lê o ID da última CVE enviada do arquivo."""
        if os.path.exists(LAST_CVE_FILE):
            try:
                with open(LAST_CVE_FILE, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Erro ao ler arquivo de persistência: {e}")
        return None

    def save_last_cve_id(self, cve_id):
        """Salva o ID da última CVE enviada."""
        try:
            with open(LAST_CVE_FILE, 'w') as f:
                f.write(cve_id)
        except Exception as e:
            logger.error(f"Erro ao salvar persistência: {e}")

    def create_cve_embed(self, cve_item):
        """Cria um Embed do Discord formatado."""
        cve = cve_item['cve']
        cve_id = cve.get('id', 'N/A')
        published = cve.get('published', 'N/A')
        descriptions = cve.get('descriptions', [])
        
        # Pega a descrição em inglês
        desc_text = "Sem descrição disponível."
        for d in descriptions:
            if d.get('lang') == 'en':
                desc_text = d.get('value')
                break
        
        # Tenta extrair métricas CVSS V3.1
        metrics = cve.get('metrics', {})
        cvss_data = {}
        score = "N/A"
        severity = "N/A"
        
        if 'cvssMetricV31' in metrics:
            cvss_data = metrics['cvssMetricV31'][0].get('cvssData', {})
            score = cvss_data.get('baseScore', 'N/A')
            severity = cvss_data.get('baseSeverity', 'N/A')
        elif 'cvssMetricV30' in metrics: # Fallback para V3.0
            cvss_data = metrics['cvssMetricV30'][0].get('cvssData', {})
            score = cvss_data.get('baseScore', 'N/A')
            severity = cvss_data.get('baseSeverity', 'N/A')
        elif 'cvssMetricV2' in metrics: # Fallback para V2
            cvss_data = metrics['cvssMetricV2'][0].get('cvssData', {})
            score = cvss_data.get('baseScore', 'N/A')
            severity = metrics['cvssMetricV2'][0].get('baseSeverity', 'N/A')

        # Define cor baseada na severidade
        color = discord.Color.blue()
        if isinstance(severity, str):
            sev_upper = severity.upper()
            if sev_upper in ['CRITICAL', 'HIGH']:
                color = discord.Color.red()
            elif sev_upper == 'MEDIUM':
                color = discord.Color.orange()
            elif sev_upper == 'LOW':
                color = discord.Color.green()

        embed = discord.Embed(
            title=f"⚠️ CVE Detectada: {cve_id} ⚠️",
            description=desc_text[:4000], # Limite do Discord
            color=color,
            url=f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        )
        
        embed.add_field(name="Publicado em (UTC)", value=published, inline=True)
        embed.add_field(name="Severidade", value=f"{severity} (Score: {score})", inline=True)
        embed.set_footer(text="Brazukas Hacking Club • Dados via NIST NVD API")
        embed.set_thumbnail(url="https://i.imgur.com/QfZQsBr.png")
        
        return embed

if __name__ == '__main__':
    intents = discord.Intents.default()
    # Não precisamos de message_content se não vamos ler comandos, mas é bom ter
    intents.messages = True 
    
    client = CVEBot(intents=intents)
    
    if TOKEN:
        client.run(TOKEN)
    else:
        logger.error("Token não encontrado. Verifique o arquivo .env")
