# Análise e Mitigação de Ataques de Negação de Serviço em Aplicações Web Modernas

## Descrição do Projeto

Este repositório contém um projeto acadêmico completo sobre Segurança da Informação, focado na análise prática de vulnerabilidades a ataques de **Negação de Serviço (DoS)**.

O estudo envolveu um processo de três etapas:

1.  **Construção** de um servidor web alvo utilizando Python e o framework moderno FastAPI.
2.  **Containerização** da aplicação com Docker para criar um ambiente de teste controlado, e a **execução** de múltiplos vetores de ataque (Camada 4 e Camada 7) utilizando ferramentas como `hping3`, `siege` e `slowhttptest`.
3.  **Análise** dos resultados e a **proposição** de contramedidas e soluções arquiteturais para mitigar as vulnerabilidades encontradas e fortalecer o servidor.

## Relatórios Detalhados das Etapas

A documentação completa do projeto está dividida nos relatórios de cada etapa, detalhando os objetivos, metodologias e conclusões de cada fase.

  * 📄 **[Relatório da Etapa 1: Desenvolvimento do Servidor Alvo](https://docs.google.com/document/d/13tBxKG-SxTeRZohuBgO7M66APglamj_vN88MOGzasJY/edit?usp=sharing.md)**
  * 📄 **[Relatório da Etapa 2: Containerização e Execução dos Ataques](https://docs.google.com/document/d/1XIYH8dEBhaBi1Q9IcSigziiCimm67kksAwmftdiQ3cg/edit?usp=sharing.md)**
  * 📄 **[Relatório da Etapa 3: Implementação de Contramedidas e Mitigações](https://docs.google.com/document/d/1LWw8H-yUP-EBd532bUWWw4p30R29U2CElCZzq0Hztis/edit?usp=sharing.md)**

## Arquitetura de Solução Proposta



## Tecnologias Utilizadas

  * **Aplicação:** Python, FastAPI, Uvicorn, Psutil
  * **Containerização:** Docker
  * **Segurança (HTTPS):** OpenSSL
  * **Ambiente de Ataque:** Windows 11 com WSL 2 (Ubuntu)
  * **Ferramentas de Ataque:**
      * `hping3` (Ataque de Camada 4)
      * `siege` (Ataque de Camada 7 - Saturação)
      * `slowhttptest` (Ataque de Camada 7 - Conexão Lenta)

## Como Executar os Testes

Para reproduzir o ambiente de teste da **Etapa 2**:

#### Pré-requisitos

  * Python 3.7+
  * Docker Desktop
  * Git for Windows (para ter o `openssl`)
  * WSL 2 com uma distribuição Linux (ex: Ubuntu)

#### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/GabrielKOP/Simulacao-de-Ataque-de-Negacao-de-Servico
    cd Simulacao-de-Ataque-de-Negacao-de-Servico
    ```
2.  **Gere os certificados SSL** (se for testar a versão HTTPS no contêiner):
    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes
    ```
3.  **Construa a imagem Docker:**
    ```bash
    docker build -t meu-servidor-fastapi .
    ```
4.  **Inicie o contêiner:**
    ```bash
    docker run -d -p 8080:8000 --memory="6g" --name meu_servidor_rodando meu-servidor-fastapi
    ```
5.  **Instale as ferramentas de ataque no WSL (Ubuntu):**
    ```bash
    sudo apt update && sudo apt install hping3 siege slowhttptest -y
    ```

Com o ambiente pronto, você pode executar os comandos de ataque detalhados no **Relatório da Etapa 2**.

## Principais Conclusões do Projeto

1.  **Resiliência a Ataques de Rede (Camada 4):** A stack moderna (Kernel Linux + Docker) demonstrou alta resiliência contra ataques clássicos de SYN Flood, mitigando-os eficazmente através de mecanismos como SYN Cookies.
2.  **Vulnerabilidade na Aplicação (Camada 7):** A principal fraqueza do sistema reside na lógica da aplicação. Endpoints mal projetados que causam **exaustão de CPU** ou **esgotamento do pool de conexões** foram os vetores de ataque mais eficazes.
3.  **Importância da Arquitetura Defensiva:** A mitigação eficaz de ataques de Camada 7 exige mais do que firewalls. É necessário um design de aplicação defensivo, com descarregamento de tarefas pesadas (task queues) e o uso de um **Reverse Proxy** para gerenciar timeouts e limitar a taxa de requisições.

## Aviso Ético

Este projeto e suas ferramentas são destinados **estritamente para fins educacionais** em ambientes controlados. A execução de ataques contra sistemas sem autorização explícita é ilegal.

##  Autor

  * **Gabriel Kauan Oliveira Pavan**
