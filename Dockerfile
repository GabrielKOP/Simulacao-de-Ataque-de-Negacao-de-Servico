# 1. Imagem Base
FROM python:3.10-slim

# 2. Diretório de Trabalho: Criar uma pasta /app dentro do contêiner e entrar nela.
WORKDIR /app

# 3. Copiar e Instalar Dependências.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o Código e os Certificados: Esta linha agora copia TUDO do diretório atual.
COPY . .

# 5. Expor a Porta que a aplicação vai usar dentro do contêiner.
EXPOSE 8000

# 6. Comando de Execução:
# --- Comando de Execução ---
# Escolha UMA das linhas abaixo e descomente (remova o #) para definir


# OPÇÃO A: Iniciar o servidor VULNERÁVEL em modo HTTPS
#CMD ["uvicorn", "main_vulneravel:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "./key.pem", "--ssl-certfile", "./cert.pem"]

# OPÇÃO B: Iniciar o servidor COM CONTRAMEDIDAS em modo HTTPS
CMD ["uvicorn", "main_com_contramedidas:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "./key.pem", "--ssl-certfile", "./cert.pem"]
