import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1_router import router as v1_router
from app.core.database import init_db
from app.worker.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing async database...")
    await init_db()
    
    logger.info("Starting autonomous background scheduler...")
    start_scheduler()
    
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AETHER Geospatial AI - Backend API",
    lifespan=lifespan
)

app.include_router(v1_router, prefix="/api/v1", tags=["Geospatial Analysis"])

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "online", "system": "AETHER CORE", "environment": settings.ENVIRONMENT}

# ==============================================================================
# INTEGRAÇÃO COM OS CRITÉRIOS DA GLOBAL SOLUTION (MENU INTERATIVO NO TERMINAL)
# ==============================================================================

import os
import asyncio
import sys

# Força o terminal do Windows a aceitar Emojis em UTF-8 (corrige o UnicodeEncodeError)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Estrutura de dados (lista) para armazenar histórico em memória
historico_pesquisas = []

def limpar_tela():
    """Limpa a tela do terminal (Usabilidade)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_descricao():
    """Exibe a descrição textual da solução (máx 5 linhas)."""
    print("=" * 70)
    print(" " * 25 + "AETHER" + " " * 25)
    print("=" * 70)
    print("AETHER é uma plataforma de Inteligência Artificial Geoespacial")
    print("focada na previsão de riscos climáticos, como enchentes. O")
    print("sistema analisa dados meteorológicos e geográficos para")
    print("gerar alertas antecipados, mitigando impactos em áreas")
    print("vulneráveis e auxiliando na tomada de decisão em tempo real.")
    print("=" * 70)

def iniciar_servidor_web():
    """Inicia o servidor FastAPI completo do AETHER."""
    print("Iniciando o servidor FastAPI (AETHER CORE)...")
    print("Acesse http://127.0.0.1:8000/docs para ver a API no navegador.")
    print("Pressione Ctrl+C no terminal para parar o servidor e voltar ao menu.")
    import uvicorn
    # Executa o servidor em localhost (127.0.0.1 evita bloqueios de Firewall no Windows)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)

async def executar_analise_real(cidade: str) -> bool:
    """
    Simula e integra a inteligência artificial climática via terminal.
    Usa subalgoritmos importados do próprio projeto (Geocoding, OpenMeteo, XGBoost).
    """
    from app.services.geocoder import Geocoder
    from app.data_pipeline.open_meteo import OpenMeteoClient
    from app.ai.climate_analyzer import ClimateAnalyzer
    from app.geospatial.processor import GeospatialProcessor
    
    # Limpa o cache para evitar erro de 'Event loop is closed' em buscas repetidas
    Geocoder.geocode.cache_clear()
    OpenMeteoClient.get_environmental_data.cache_clear()
    
    print(f"\nBuscando coordenadas para '{cidade}'...")
    geo = await Geocoder.geocode(cidade)
    
    # Decisão: if-else
    if not geo:
        print("Erro: Cidade não encontrada. Verifique o nome digitado.")
        return False
        
    lat, lon = geo["latitude"], geo["longitude"]
    print(f"Encontrado: {geo['display_name']} (Lat: {lat}, Lon: {lon})")
    
    print("Coletando dados meteorológicos em tempo real (Open-Meteo)...")
    climate_data = await OpenMeteoClient.get_environmental_data(lat, lon)
    
    print("Processando inteligência artificial climática (ODS 13)...")
    analyzer = ClimateAnalyzer()
    slope = GeospatialProcessor.calculate_slope(climate_data.get("elevation", 0))
    
    riscos = analyzer.analyze_all_risks(climate_data, slope)
    risco_principal = riscos[0] # Maior ameaça calculada
    
    resultado = {
        "cidade": geo["display_name"],
        "risco_principal": risco_principal["risk_type"],
        "severidade": risco_principal["severity"],
        "probabilidade": f"{risco_principal['probability_percent']}%"
    }
    # Manipulação de lista (append)
    historico_pesquisas.append(resultado)
    
    print("\n" + "=" * 60)
    print(f"RESULTADO DA ANÁLISE: {geo['display_name']}")
    print(f"Maior Ameaça: {risco_principal['risk_icon']} {risco_principal['risk_type']}")
    print(f"Nível de Severidade: {risco_principal['severity_icon']} {risco_principal['severity']}")
    print(f"Probabilidade: {risco_principal['probability_percent']}%")
    print(f"Recomendação: {risco_principal['recommendation']}")
    print("=" * 60)
    
    # Fecha os clientes HTTP para não dar crash ("Event loop is closed") na próxima consulta no terminal
    if getattr(Geocoder, "_client", None):
        await Geocoder._client.aclose()
        Geocoder._client = None
    if getattr(OpenMeteoClient, "_client", None):
        await OpenMeteoClient._client.aclose()
        OpenMeteoClient._client = None
        
    return True

def listar_historico() -> list:
    """Retorna a lista do histórico."""
    return historico_pesquisas

def filtrar_historico(nivel: str) -> list:
    """
    Filtra o histórico por nível de severidade.
    Demonstra laço de repetição (for) e manipulação de strings.
    """
    filtrados = []
    for item in historico_pesquisas:
        if nivel.lower() in item['severidade'].lower():
            filtrados.append(item)
    return filtrados

def gerar_relatorio_estatistico() -> bool:
    """
    Gera um resumo estatístico das análises realizadas na sessão.
    Demonstra uso explícito de if-elif-else, contadores e manipulação de lista.
    """
    if not historico_pesquisas:
        print("\nNenhum dado no histórico para gerar relatório.")
        return False
        
    total = len(historico_pesquisas)
    criticos = 0
    altos = 0
    outros = 0
    
    # Estrutura de repetição
    for item in historico_pesquisas:
        # Estrutura de decisão encadeada exigida pelos critérios: if-elif-else
        if "CRÍTICO" in item['severidade'].upper():
            criticos += 1
        elif "ALTO" in item['severidade'].upper():
            altos += 1
        else:
            outros += 1
            
    print("=" * 60)
    print(" " * 12 + "RELATÓRIO ESTATÍSTICO DE ALERTAS" + " " * 12)
    print("=" * 60)
    print(f"Total de Análises na Sessão: {total}")
    print(f"- Regiões em Estado CRÍTICO: {criticos}")
    print(f"- Regiões em Estado ALTO:    {altos}")
    print(f"- Regiões Seguras/Moderadas: {outros}")
    
    # Segunda validação if-elif-else baseada nos resultados
    if criticos > 0:
        print("\n>>> ALERTA GLOBAL: Há regiões exigindo intervenção emergencial da Defesa Civil!")
    elif altos > 0:
        print("\n>>> AVISO: Mantenha forte vigilância nas regiões de alto risco.")
    else:
        print("\n>>> STATUS: Nenhuma das regiões analisadas apresenta perigo crítico imediato.")
    print("=" * 60)
    return True

def exibir_menu_interativo():
    """Menu interativo principal em loop (while)."""
    while True:
        limpar_tela()
        print("=" * 70)
        print(" " * 18 + "MENU AETHER - GLOBAL SOLUTION" + " " * 18)
        print("=" * 70)
        print("1. Descrição da Solução Proposta")
        print("2. Ligar Servidor Backend Completo (FastAPI)")
        print("3. Executar Análise Climática Real (Requer Internet)")
        print("4. Listar Histórico de Consultas da Sessão")
        print("5. Filtrar Histórico por Severidade")
        print("6. Gerar Relatório Estatístico")
        print("0. Sair do Sistema")
        print("=" * 70)
        
        opcao = input("\nEscolha uma opção (0-6): ")
        
        # Estrutura de seleção: match-case
        match opcao:
            case '1':
                limpar_tela()
                exibir_descricao()
                input("\nPressione ENTER para voltar ao menu...")
            case '2':
                limpar_tela()
                iniciar_servidor_web()
                input("\nPressione ENTER para voltar ao menu...")
            case '3':
                limpar_tela()
                print("--- ANÁLISE CLIMÁTICA EM TEMPO REAL ---")
                cidade = input("Digite o nome da cidade/região (ex: Recife, PE): ")
                asyncio.run(executar_analise_real(cidade))
                input("\nPressione ENTER para voltar ao menu...")
            case '4':
                limpar_tela()
                print("--- HISTÓRICO DE CONSULTAS ---")
                lista = listar_historico()
                if not lista:
                    print("Nenhuma consulta realizada nesta sessão.")
                else:
                    # Usabilidade: formatação tabulada
                    print(f"{'CIDADE':<35} | {'AMEAÇA':<25} | {'SEVERIDADE'}")
                    print("-" * 80)
                    for item in lista:
                        print(f"{item['cidade'][:33]:<35} | {item['risco_principal']:<25} | {item['severidade']}")
                input("\nPressione ENTER para voltar ao menu...")
            case '5':
                limpar_tela()
                print("--- FILTRAR HISTÓRICO ---")
                nivel = input("Digite a severidade (BAIXO, MODERADO, ALTO, CRÍTICO): ")
                resultados = filtrar_historico(nivel)
                if not resultados:
                    print(f"\nNenhum registro encontrado com a palavra '{nivel}'.")
                else:
                    print(f"\nResultados contendo '{nivel}':")
                    print("-" * 50)
                    for res in resultados:
                        print(f"- {res['cidade']} -> {res['risco_principal']} ({res['severidade']})")
                input("\nPressione ENTER para voltar ao menu...")
            case '6':
                limpar_tela()
                print("--- GERAÇÃO DE RELATÓRIO ESTATÍSTICO ---")
                gerar_relatorio_estatistico()
                input("\nPressione ENTER para voltar ao menu...")
            case '0':
                limpar_tela()
                print("Encerrando AETHER CLI. Até logo!")
                break
            case _:
                print("\nOpção inválida! Escolha de 0 a 6.")
                input("\nPressione ENTER para tentar novamente...")

if __name__ == "__main__":
    # Ao executar `python app/main.py`, o menu interativo será aberto.
    exibir_menu_interativo()