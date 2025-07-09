import time
import psutil
import os
import datetime
from fastapi import FastAPI, Request

# Cria a instância da aplicação FastAPI
# O título e a versão aparecerão na documentação automática.
app = FastAPI(
    title="Servidor Funcional com FastAPI",
    description="Um servidor de exemplo mais completo e seguro com HTTPS.",
    version="1.0.0",
)

# Métricas simples para monitoramento
server_start_time = datetime.datetime.now()
request_counter = 0

# Middleware para contar requisições (uma forma mais elegante)
@app.middleware("http")
async def count_requests(request: Request, call_next):
    global request_counter
    request_counter += 1
    response = await call_next(request)
    return response

# --- Nossos Endpoints ---

@app.get("/", summary="Página Inicial")
def read_root():
    """
    Retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo ao servidor FastAPI com HTTPS!"}

@app.get("/api/info", summary="Endpoint de API")
def get_api_info():
    """
    Simula um endpoint de API que retorna dados JSON.
    """
    time.sleep(0.1) # Simula trabalho
    return {
        "versao": "1.0",
        "status": "online",
        "timestamp": time.time(),
    }

@app.get("/pagina_pesada", summary="Página com Processamento Pesado")
def get_heavy_page():
    """
    Simula um endpoint que realiza um trabalho computacionalmente intensivo.
    """
    print("Iniciando processamento pesado...")
    time.sleep(1.5) # Simula trabalho pesado
    print("Processamento pesado concluído.")
    return {"message": "Página pesada processada com sucesso após 1.5 segundos."}

@app.get("/status", summary="Status e Métricas do Servidor")
def get_server_status():
    """
    Retorna métricas de saúde e performance do servidor usando psutil.
    """
    process = psutil.Process(os.getpid())
    uptime = datetime.datetime.now() - server_start_time
    
    return {
        "server_status": "online",
        "uptime_seconds": uptime.total_seconds(),
        "cpu_usage_percent": process.cpu_percent(interval=0.1),
        "memory_usage_mb": process.memory_info().rss / (1024 * 1024),
        "total_requests_received": request_counter,
    }

@app.get("/cpu_pesada", summary="Endpoint que consome 100% da CPU")
def get_cpu_intensive():
    """
    Simula um trabalho computacionalmente intensivo que consome CPU.
    """
    print("Iniciando processamento de CPU pesado...")
    # Um loop simples para gastar ciclos de CPU, calculando o quadrado de 20 milhões de números.
    # Este cálculo é "CPU-bound", ou seja, limitado pela velocidade do processador.
    resultado = [x**2 for x in range(20_000_000)]
    print("Processamento de CPU concluído.")
    return {"message": "Trabalho pesado de CPU concluído!"}