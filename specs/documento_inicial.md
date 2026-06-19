# Documento Inicial - Trabalho Final de APIs para IA

Este documento detalha o escopo e o planejamento para o Trabalho Final da disciplina de Construção de APIs para Inteligência Artificial, conforme solicitado pelo professor Rogério Rodrigues Carvalho.

O objetivo deste projeto é construir uma API funcional em **FastAPI** que encapsule os nossos "Agentes" (skills) de gestão contratual existentes, transformando-os em endpoints (serviços) reais.

---

## 1. Escopo do Projeto

A API disponibilizará endpoints que utilizam LLM para realizar tarefas de análise e extração de dados a partir de documentos (PDFs, Textos). As "skills" existentes no repositório (`analisador-contratual`, `analisador-sms`, `gerador-checklist`, etc.) serão expostas como serviços RESTful.

Isso cumpre o requisito principal do trabalho:
> "Desenvolver uma API funcional que disponibilize pelo menos dois serviços (endpoints) de Inteligência Artificial (IA)..."

Neste projeto, implementaremos pelo menos 3 endpoints para garantir robustez na apresentação.

### Endpoints Planejados
Todos os serviços abaixo receberão o upload de um arquivo (UploadFile) e aplicarão um prompt estruturado.
1. **`POST /api/v1/contratos/analise-contratual`**
   - **Objetivo**: Extrair cláusulas de penalidades, multas, sanções e prazos de vigência.
   - **Base**: `analisador-contratual`
2. **`POST /api/v1/contratos/analise-sms`**
   - **Objetivo**: Extrair requisitos e obrigações de Saúde, Meio Ambiente e Segurança.
   - **Base**: `analisador-sms`
3. **`POST /api/v1/contratos/gerar-checklist`**
   - **Objetivo**: Criar automaticamente um checklist de verificação para os fiscais do contrato.
   - **Base**: `gerador-checklist-contratual`

---

## 2. Atendimento aos Requisitos Obrigatórios

Para obtermos a nota máxima e cumprirmos o que foi passado no PDF, as seguintes características serão integradas ao projeto, aproveitando a estrutura base que o professor disponibilizou (`api/main.py`):

* **[x] Serviço de IA Diferenciado**: Em vez de geração de histórias (como na aula), utilizaremos os nossos próprios prompts (Agentes de Análise Contratual).
* **[x] Validação de Dados**: 
  - Restrição para que a API aceite estritamente arquivos válidos (PDF/TXT) com um limite de tamanho seguro.
  - Validação de payload usando `Pydantic`.
* **[x] Tratamento de Erros**:
  - Respostas amigáveis em caso de arquivo corrompido (HTTP 400).
  - Tratamento de falhas de comunicação com a IA (HTTP 502/500).
  - Tratamento de autenticação negada (HTTP 401).
* **[x] Logs**:
  - Adição de um sistema de `logging` detalhado registrando quando o endpoint é acessado, tempo de execução do LLM e possíveis exceções.
* **[x] Segurança**:
  - Todos os endpoints sob `/api/v1/contratos` exigirão um token Bearer válido, reaproveitando a estrutura do `auth_router.py`.
* **[x] Versionamento**:
  - Implementação de prefixo `/api/v1/` nas rotas para facilitar futuras evoluções da API.
* **[x] Documentação**:
  - Uso de tags, docstrings ricas, descrições e exemplos preenchidos para que a tela nativa do Swagger (`/docs`) e Redoc (`/redoc`) funcionem como documentação técnica da API.

---

## 3. Próximos Passos (Plano de Ação)

Para começarmos a escrever o código, o roteiro será:

1. **Reestruturação e Configuração Básica**
   - Refatorar o `main.py` e ajustar a inicialização da API (versões, títulos atualizados para o projeto).
   - Configurar o módulo de Logs centralizado.
2. **Desenvolvimento do Serviço LLM (`llm_service.py`)**
   - Criar as funções utilitárias para ler o PDF recebido na requisição HTTP.
   - Integrar com o modelo de IA que você possuir configurado (ex: OpenAI, Gemini), unindo o texto do PDF com as instruções da *skill* respectiva.
3. **Criação do Router (`contratos_router.py`)**
   - Implementar os 3 endpoints descritos.
   - Aplicar dependências de Autenticação (`Depends(get_current_active_user)`).
   - Aplicar tratamento de erros e validações de arquivos.
4. **Testes de Integração**
   - Subir a API localmente.
   - Autenticar via Swagger.
   - Realizar o upload de um PDF real de contrato e validar as respostas da IA.
5. **Preparação para Entrega**
   - Gravar o vídeo de 10 minutos (Tarefa de responsabilidade do aluno).
   - Criar o arquivo `README.md` detalhado informando como rodar a solução em outra máquina.
