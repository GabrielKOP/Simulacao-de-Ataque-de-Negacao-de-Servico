import time
import psutil
import os
import datetime
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from threading import Lock

# --- SETUP DAS CONTRAMEDIDAS ---
limiter = Limiter(key_func=get_remote_address)
MAX_CONCURRENT_HEAVY_TASKS = 4
active_heavy_tasks_counter = 0
counter_lock = Lock()

# --- SETUP DA APLICAÇÃO FASTAPI ---
app = FastAPI(
    title="Servidor Imune a Ataques de Aplicação",
    description="Um servidor com múltiplas camadas de defesa contra ataques de exaustão de recursos.",
    version="4.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- MÉTRICAS GLOBAIS (POSIÇÃO CORRIGIDA) ---
server_start_time = datetime.datetime.now()
request_counter = 0

# --- MIDDLEWARE ---
@app.middleware("http")
#@limiter.limit("1000/minute")
async def count_requests(request: Request, call_next):
    global request_counter
    request_counter += 1
    response = await call_next(request)
    return response

# --- FUNÇÃO DE TRABALHO PESADO ---
def do_heavy_calculation():
    global active_heavy_tasks_counter
    print("WORKER EM BACKGROUND: Iniciando processamento de CPU pesado...")
    try:
        for x in range(20_000_000):
            _ = x**2
    finally:
        with counter_lock:
            active_heavy_tasks_counter -= 1
        print(f"WORKER EM BACKGROUND: Processamento de CPU concluído. Tarefas ativas: {active_heavy_tasks_counter}")

# --- ENDPOINTS DO SERVIDOR ---

@app.get("/", summary="Página Inicial")
@limiter.limit("120/minute")
def read_root(request: Request):
    return {"message": "Bem-vindo ao Servidor Imune!"}

@app.get("/api/info", summary="Endpoint de API")
@limiter.limit("120/minute")
def get_api_info(request: Request):
    time.sleep(0.1)
    return {
        "versao": "4.0",
        "status": "online",
        "timestamp": time.time(),
    }

@app.get("/pagina_pesada", summary="Página com Processamento Leve (I/O)")
@limiter.limit("30/minute")
def get_heavy_page(request: Request):
    time.sleep(1.5)
    return {"message": "Página com espera I/O processada com sucesso após 1.5 segundos."}

@app.get("/status", summary="Status e Métricas do Servidor")
@limiter.limit("60/minute")
def get_server_status(request: Request):
    process = psutil.Process(os.getpid())
    uptime = datetime.datetime.now() - server_start_time
    return {
        "server_status": "online",
        "uptime_seconds": uptime.total_seconds(),
        "cpu_usage_percent": process.cpu_percent(interval=0.1),
        "memory_usage_mb": process.memory_info().rss / (1024 * 1024),
        "total_requests_received": request_counter,
        "active_heavy_tasks": active_heavy_tasks_counter,
    }

@app.get("/cpu_pesada", summary="Endpoint que AGENDA uma tarefa de CPU pesada com CONTROLE")
@limiter.limit("5/minute")
def get_cpu_intensive_with_concurrency_control(request: Request, background_tasks: BackgroundTasks):
    global active_heavy_tasks_counter
    with counter_lock:
        if active_heavy_tasks_counter >= MAX_CONCURRENT_HEAVY_TASKS:
            print(f"RECUSADO: Limite de tarefas pesadas ({MAX_CONCURRENT_HEAVY_TASKS}) atingido.")
            return JSONResponse(
                status_code=503,
                content={"message": "Serviço temporariamente sobrecarregado, tente novamente mais tarde."}
            )
        active_heavy_tasks_counter += 1
        background_tasks.add_task(do_heavy_calculation)
        print(f"ENDPOINT: Tarefa agendada. Tarefas ativas: {active_heavy_tasks_counter}")
    return {"message": "O trabalho pesado de CPU foi agendado e está rodando em segundo plano!"}