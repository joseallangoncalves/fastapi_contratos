# API de Gestão e Análise Contratual com Inteligência Artificial 📑🚀

Trabalho Final desenvolvido para a disciplina de **Construção de APIs para Inteligência Artificial**, sob orientação do professor **Rogério Rodrigues Carvalho**.

Esta API em **FastAPI** encapsula "agentes" (skills) baseados em LLM para automatizar o processo de triagem, mapeamento e análise de riscos de contratos industriais complexos (ex: padrões Petrobras/Petronect).

---

## 🛠️ Funcionalidades e Endpoints (Ordem de Ciclo de Vida)

Todos os endpoints estão agrupados no Swagger UI sob a tag `"Análise de Contratos (IA)"`, requerem **Autenticação Bearer (JWT)** e seguem um fluxo lógico sequencial:

### 1. Processamento e Criação (POST)
* **`POST /api/v1/contratos/reconhecimento-estratificacao`**
  * *Mapeamento de Layout*: Analisa o sumário e as primeiras páginas de um PDF de contrato, mapeia os intervalos de páginas de cada anexo/seção (SMS, PPU, ICJ) e identifica se a página contém texto, imagens ou ambos. Extrai o número único do contrato.
* **`POST /api/v1/contratos/ingestao-metadados`**
  * *Ingestão Cadastral*: Extrai os metadados cadastrais chaves do contrato (número do contrato, oportunidade Petronect, objeto, contratante, contratada, vigência, execução e valor global). **Não** armazena o corpo do ICJ bruto, focando estritamente nos dados de cadastro.
* **`POST /api/v1/contratos/analise-contratual`**
  * *Análise de Cláusulas*: Realiza uma leitura minuciosa do contrato para transcrever integralmente cláusulas críticas de vigência/prazo, multas moratórias, multas compensatórias, sanções administrativas e rescisão contratual.

### 2. Consulta e Recuperação (GET)
* **`GET /api/v1/contratos/reconhecimento-estratificacao`**
  * Lista todas as estratificações de páginas persistidas. Permite busca por `numero_contrato`.
* **`GET /api/v1/contratos/reconhecimento-estratificacao/{id}`**
  * Consulta os detalhes de uma estratificação específica pelo ID único.
* **`GET /api/v1/contratos/ingestao-metadados`**
  * Lista os metadados cadastrais persistidos. Permite filtros por `numero_contrato` ou `contratada`.
* **`GET /api/v1/contratos/ingestao-metadados/{id}`**
  * Consulta o registro de metadados cadastrais por ID.
* **`GET /api/v1/contratos/analises`**
  * Lista as análises de multas e vigência salvas. Permite filtros por `numero_contrato`, `cnpj` ou `empresa`.
* **`GET /api/v1/contratos/analises/{id}`**
  * Consulta detalhada de uma análise contratual específica por ID.

### 3. Edição e Exclusão (PATCH / DELETE)
* **`PATCH /api/v1/contratos/analises/{id}`**
  * Atualiza parcialmente qualquer metadado ou cláusula transcrita de uma análise contratual existente.
* **`DELETE /api/v1/contratos/analises/{id}`**
  * Exclui uma análise contratual do banco de dados (exige o parâmetro query string `confirm=true` para efetivar).

---

## 🛡️ Validações e Regras de Robustez (Boas Práticas)

* **Prazos em Dias**: Todos os prazos de vigência e prazos de execução são processados, armazenados e validados estritamente na unidade de **dias** (números inteiros positivos) para suportar com precisão o linguajar de contratos industriais (ex: prazos de `1115 dias`). A data de término é calculada dinamicamente com base nesse número.
* **Sanitização Inteligente de Busca**: A filtragem de listagens por número do contrato ou CNPJ remove automaticamente espaços, pontos (`.`), traços (`-`), barras (`/`) e o prefixo `ICJ` tanto na entrada do usuário quanto no banco de dados. Isso significa que buscar `59000132964252` trará com sucesso o contrato registrado como `ICJ 5900.0132964.25.2`.
* **Validação de Tamanho (14 dígitos)**: Se o usuário preencher o filtro de contrato ou CNPJ na busca, a API exige **exatamente 14 dígitos numéricos**. Entradas incompletas ou excessivas retornam erro **`400 Bad Request`** com mensagem explicativa.
* **Upload Seguro**: Os endpoints de POST aceitam apenas arquivos no formato **PDF** (`.pdf`) com um tamanho máximo de **50 MB**.
* **Documentação Autogerada Enriquecida**: Todos os endpoints, parâmetros de busca, parâmetros de path e payloads de requisição/resposta do Swagger contêm descrições e exemplos claros em português para facilitar testes imediatos.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.12+
* Gerenciador de dependências [uv](https://docs.astral.sh/uv/)

### 1. Configurando Variáveis de Ambiente
Faça uma cópia do arquivo `.env.sample` para `.env` e preencha as variáveis de ambiente necessárias (como a chave de API do GROQ e o `SECRET_KEY` para geração de tokens de autenticação).
```bash
cp .env.sample .env
```

### 2. Instalação das Dependências
Instale as dependências sincronizadas no ambiente virtual local usando o `uv`:
```bash
uv sync
```

### 3. Executando o Servidor de Desenvolvimento
Inicie a aplicação FastAPI localmente:
```bash
uv run fastapi dev api/main.py
```
*(Nota: O banco de dados SQLite `contratos.db` é criado e migrado de forma automática na primeira inicialização).*

### 4. Acessando a Documentação
* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

---

## 🔑 Credenciais Fictícias para Avaliação

Para testar o fluxo de autenticação e obter o token de acesso (JWT) no Swagger UI, clique no botão **Authorize** no topo do Swagger e informe:
* **Username:** `johndoe`
* **Password:** `secret`
