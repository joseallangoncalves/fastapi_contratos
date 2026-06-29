# Roteiro de Apresentação — API de Análise de Contratos com IA

**Disciplina:** Construção de APIs para Inteligência Artificial  
**Equipe:** José Allan, Elson, PH, Geiziane  
**Duração:** Até 10 minutos

---

## Bloco 1 — Contexto e Motivação (~1 min)

**Fala sugerida:**
> "Olá, nosso grupo desenvolveu uma API para automatizar a análise de contratos industriais. O problema real é que contratos complexos, como os padrões Petrobras, possuem múltiplos anexos — Instrumento Contratual Jurídico, Memorial Descritivo, SMS, Planilha de Preços. A análise manual é lenta, propensa a erros e consome horas de profissionais especializados. Nossa API resolve isso usando Inteligência Artificial para extrair e estruturar automaticamente as informações desses documentos."

**Na tela:**
- Mostrar um contrato PDF exemplo com vários anexos
- Destacar a complexidade visual

---

## Bloco 2 — Visão Geral da Arquitetura (~1 min)

**Fala sugerida:**
> "A arquitetura segue o padrão de camadas do FastAPI. O cliente faz requisições HTTP que passam pelo middleware de autenticação JWT, são roteadas para os endpoints, que delegam a lógica de IA para um service layer, que se comunica com o Google Gemini. Os resultados são persistidos em SQLite via SQLAlchemy."

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐
│ Cliente │────▶│ FastAPI  │────▶│ Router   │────▶│ LLM Service │
└─────────┘     └──────────┘     └──────────┘     └──────┬──────┘
                      │                                       │
                      ▼                                       ▼
               ┌──────────┐                          ┌─────────────┐
               │ JWT Auth │                          │    Gemini   │
               │ (Argon2) │                          │     API     │
               └──────────┘                          └─────────────┘
                      │                                       │
                      ▼                                       ▼
               ┌──────────┐                          ┌─────────────┐
               │ SQLite   │                          │   Pydantic  │
               │ (SQLAlch.)│                          │ (validação) │
               └──────────┘                          └─────────────┘
```

**Na tela:** Diagrama da arquitetura

---

## Bloco 3 — Demonstração Funcional (~4 min)

### 3.1 Autenticação (~30s)

**Fala sugerida:**
> "Antes de usar os endpoints de IA, precisamos nos autenticar. Vou acessar o Swagger UI e usar as credenciais de teste para obter um token JWT."

**Na tela:**
- Abrir `http://localhost:8000/docs`
- Clicar em `Authorize`, inserir `johndoe` / `secret`
- Mostrar o botão Authorize ficando verde

### 3.2 Endpoint 1 — Ingestão de Metadados (~1 min 30s)

**Fala sugerida:**
> "Primeiro serviço de IA: extração de metadados cadastrais. Vou fazer upload de um contrato PDF e a API retorna os dados estruturados: número do contrato, contratante, contratada, objeto, prazos e valor total. Tudo extraído automaticamente pelo Gemini."

**Na tela:**
- `POST /api/v1/contratos/ingestao-metadados`
- Escolher arquivo PDF
- Mostrar resposta JSON:
```json
{
  "numero_contrato": "5900.0132964.25.2",
  "contratante": "Petrobras",
  "contratada": "Empresa Exemplo Ltda",
  "objeto_contrato": "Prestação de serviços de manutenção...",
  "prazo_vigencia": 1115,
  "prazo_execucao": 1095,
  "valor_total": "R$ 12.345.678,90"
}
```

### 3.3 Endpoint 2 — Análise Contratual (~1 min 30s)

**Fala sugerida:**
> "Segundo serviço: análise de cláusulas críticas. Enquanto o primeiro extrai dados cadastrais, este faz uma leitura minuciosa do contrato para transcrever cláusulas de multas, sanções e rescisão. São operações diferentes com prompts diferentes."

**Na tela:**
- `POST /api/v1/contratos/analise-contratual`
- Upload do mesmo PDF
- Mostrar resposta destacando cláusulas de multa moratória, sanções administrativas

### 3.4 Consulta aos dados persistidos (~30s)

**Fala sugerida:**
> "Todos os resultados são persistidos no SQLite. Posso consultar histórico, filtrar por número de contrato e até atualizar ou excluir registros."

**Na tela:**
- `GET /api/v1/contratos/analises` — listar registros
- `GET /api/v1/contratos/analises/1` — detalhe de um registro

---

## Bloco 4 — Características Técnicas (~2 min)

Mostrar no código (VS Code aberto). Para cada item, mostrar a tela do código e explicar brevemente.

| Característica | Arquivo | O que mostrar |
|---|---|---|
| **Validação de dados** | `api/models.py` | `@field_validator("prazo_vigencia")` garantindo inteiro positivo |
| **Tratamento de erros** | `api/services/llm_service.py` | `raise HTTPException(400, "Formato inválido")` para PDF inválido |
| **Logs** | `api/utils.py` | `logger.info("Processando documento...")` com timestamp |
| **Segurança** | `api/routers/auth_router.py` | JWT com HS256, Argon2, dummy hash para timing attack |
| **Fallback de IA** | `api/utils.py` | `FALLBACK_MODELS` com retry exponencial em caso de rate limit |
| **Esquema estruturado** | `api/services/llm_service.py` | `response_schema=PydanticModel` forçando JSON estruturado do Gemini |

**Fala sugerida (exemplo para validação):**
> "Aqui no Pydantic usamos validadores para garantir que prazos sejam sempre números inteiros positivos. Se alguém tentar enviar um prazo negativo, a API rejeita automaticamente com uma mensagem clara."

---

## Bloco 5 — Testes e Qualidade (~1 min)

**Fala sugerida:**
> "Para garantir a qualidade, implementamos testes automatizados com pytest que cobrem health check, autenticação, validação de erros e chamadas aos endpoints de IA."

Mostrar (se houver):
- `pytest` rodando e passando
- Ou `ruff check .` mostrando zero erros

**Fala sugerida:**
> "Usamos ruff como linter, pre-commit hooks para padronização, e conventional commits no GitHub para versionamento semântico."

**Na tela:**
- Resultado do terminal com `ruff check .`
- GitHub com histórico de commits

---

## Bloco 6 — Como Executar (~30s)

**Fala sugerida:**
> "Para executar em qualquer máquina, basta ter Python 3.12 e uv instalados. Copie o .env.sample, configure a GEMINI_API_KEY, instale as dependências com uv sync e execute com uv run fastapi dev api/main.py."

```bash
cp .env.sample .env
# Editar .env com GEMINI_API_KEY
uv sync
uv run fastapi dev api/main.py
```

**Na tela:**
- Terminal executando os comandos

---

## Bloco 7 — Encerramento (~30s)

**Fala sugerida:**
> "O código está disponível no GitHub com README completo, documentação OpenAPI interativa no Swagger e Redoc. Agradecemos a atenção e estamos à disposição para perguntas."

**Na tela:**
- Repositório no GitHub aberto
- QR code ou link: `https://github.com/.../fastapi_contratos`

---

## Dicas Técnicas para Gravação

| Item | Recomendação |
|---|---|
| **Ferramenta** | OBS Studio (gratuito) ou Loom (já hospeda) |
| **Layout** | Tela dividida: Swagger UI (esquerda) + VS Code (direita) |
| **PDF de teste** | Use um contrato real com dados anônimos |
| **Câmera** | Opcional, mas ajuda na conexão |
| **Mostrar erro também** | Envie um arquivo .txt no lugar de .pdf para mostrar tratamento de erro |
| **Edição** | Corte pausas longas, mas mantenha ritmo natural |
| **Áudio** | Microfone com bom isolamento, grave em ambiente silencioso |

---

## Checklist Pré-Gravação

- [ ] API rodando localmente
- [ ] Swagger UI acessível em `http://localhost:8000/docs`
- [ ] PDF de contrato para upload
- [ ] VS Code aberto com os arquivos principais
- [ ] GitHub do repositório aberto
- [ ] Terminal com `ruff check` zerado
- [ ] Testes pytest passando (se houver)
- [ ] .env com GEMINI_API_KEY configurada
