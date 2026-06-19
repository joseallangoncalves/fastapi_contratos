# API de Análise de Contratos (Trabalho Final)

Repositório da API desenvolvida para o Trabalho Final da disciplina de Construção de APIs para Inteligência Artificial.

A API integra "agentes" (skills) baseados em LLM para realizar a extração e análise de informações de contratos em PDF.

## Funcionalidades (Endpoints)

Todos os serviços abaixo estão disponíveis em `/api/v1/contratos` e requerem Autenticação (Token JWT via OAuth2):

- `POST /analise-contratual`: Extrai penalidades, multas, sanções e vigência.
- `POST /analise-sms`: Identifica regras de Segurança, Meio Ambiente e Saúde aplicáveis à Contratada.
- `POST /gerar-checklist`: Cria uma lista de verificações para fiscalização contratual.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Criação do arquivo .env

Faça uma cópia do arquivo `.env.sample` para `.env` e preencha as variáveis de ambiente necessárias (como a chave de API do GROQ e o SECRET_KEY para autenticação).

## Instalação de dependências

```bash
uv sync
```

## Executar a aplicação localmente

```bash
uv run fastapi dev api\main.py
```

Ou, caso já esteja com o ambiente virtual ativado:
```bash
fastapi dev api\main.py
```

A aplicação estará disponível em: http://localhost:8000
A documentação interativa (Swagger UI) estará em: http://localhost:8000/docs
