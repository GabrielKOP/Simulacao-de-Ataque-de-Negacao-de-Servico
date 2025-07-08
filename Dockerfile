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

# 6. Comando de Execução (MODIFICADO): Adicionamos as flags de SSL.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "./key.pem", "--ssl-certfile", "./cert.pem"]
