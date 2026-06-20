# Especificação Técnica: Persistência de Análises Contratuais

Esta especificação descreve a implementação da persistência automática dos resultados gerados pelo **Analisador Contratual** em um banco de dados SQLite local.

---

## 1. Motivação e Objetivos

Ao realizar a análise de um contrato através do endpoint `/api/v1/contratos/analise-contratual`, os dados extraídos pelo modelo de linguagem (LLM) devem ser salvos de forma estruturada. Isso permitirá a posterior consulta, comparação e consolidação de indicadores fundamentais, tais como:
* Identificação da empresa e CNPJ.
* Prazos de vigência (datas de início e término).
* Valor total do contrato.
* **Cláusulas Literais (na íntegra):** O trecho textual exato de cada cláusula mapeada no contrato (vigência, multas, sanções, rescisão) para evitar a necessidade de reavaliar o PDF todas as vezes.

---

## 2. Arquitetura da Solução

### Banco de Dados
* **Tecnologia:** SQLite (banco em arquivo `contratos.db` na raiz do projeto).
* **ORM:** SQLAlchemy para modelagem das tabelas, controle de conexões e migração simplificada (criação automática das tabelas na inicialização da aplicação).

### Fluxo de Execução no Endpoint `/analise-contratual`
1. O usuário envia o contrato em formato PDF.
2. O sistema extrai o texto bruto do PDF.
3. **Análise de Texto (Relatório):** O LLM gera o relatório detalhado em Markdown (mantendo o comportamento atual).
4. **Extração Estruturada (Metadados e Cláusulas Literais):** Em paralelo ou logo após a geração do relatório, uma chamada estruturada ao LLM (usando o recurso de *Structured Outputs* da API do Gemini) extrairá os campos específicos em formato JSON mapeado para uma classe `Pydantic`.
5. **Persistência:** Os dados estruturados são inseridos na tabela `analises_contratuais` junto com o timestamp atual de inserção.
6. A API retorna o relatório em Markdown e, opcionalmente, um identificador ou resumo dos dados salvos no banco.

---

## 3. Estrutura do Banco de Dados

### Tabela `analises_contratuais`

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER (PK) | Chave primária autoincrementada. |
| `empresa` | VARCHAR | Nome da empresa contratada. |
| `cnpj` | VARCHAR | CNPJ da empresa contratada. |
| `data_inicio` | VARCHAR | Data de início da vigência do contrato. |
| `data_fim` | VARCHAR | Data de término da vigência do contrato. |
| `valor_contrato` | VARCHAR | Valor total ou estimado do contrato. |
| `data_insercao` | DATETIME | Data e hora em que a análise foi persistida no banco. |
| `vigencia_prazo` | TEXT | Item 1 da Skill: Vigência e Prazo (cláusula textual literal extraída do contrato). |
| `multas_moratorias` | TEXT | Item 2 da Skill: Multas Moratórias (cláusula textual literal extraída do contrato). |
| `multas_compensatorias` | TEXT | Item 3 da Skill: Multas Compensatórias (cláusula textual literal extraída do contrato). |
| `sancoes_administrativas` | TEXT | Item 4 da Skill: Sanções Administrativas (cláusula textual literal extraída do contrato). |
| `rescisao` | TEXT | Item 5 da Skill: Condições de Rescisão (cláusula textual literal extraída do contrato). |

---

## 4. Endpoints Novos e Modificados

### 1. Modificação: `POST /api/v1/contratos/analise-contratual`
* **Input:** `file` (UploadFile)
* **Comportamento adicional:** Dispara a extração estruturada via LLM e insere o registro no SQLite.
* **Output:**
  ```json
  {
    "id_analise": 1,
    "analise": "## RELATÓRIO DE PENALIDADES...",
    "dados_salvos": {
      "empresa": "Empresa Teste Ltda",
      "cnpj": "00.000.000/0001-00",
      "data_inicio": "2026-01-01",
      "data_fim": "2027-01-01",
      "valor_contrato": "R$ 150.000,00"
    }
  }
  ```

### 2. Novo Endpoint: `GET /api/v1/contratos/analises`
* **Descrição:** Recupera a lista de todas as análises salvas no banco.
* **Query Params opcionais:** `empresa`, `cnpj` (para filtragem).
* **Response:** Lista de objetos contendo os dados estruturados salvos.

### 3. Novo Endpoint: `GET /api/v1/contratos/analises/{id}`
* **Descrição:** Recupera os detalhes completos de uma análise específica pelo ID.

---

## 5. Implementação Técnica

### Alteração nas Dependências (`pyproject.toml`)
Adicionaremos o SQLAlchemy para facilitar o gerenciamento do banco:
```toml
dependencies = [
    ...
    "sqlalchemy>=2.0.0",
]
```

### Novo Módulo: `api/database.py`
Instanciação do `engine` do SQLAlchemy, definição do `SessionLocal` e da base declarativa para criação automática da tabela na inicialização do FastAPI.

### Modificação no Serviço: `api/services/llm_service.py`
Função dedicada a realizar a chamada estruturada do Gemini para extrair metadados e trechos de cláusulas literais na íntegra:
```python
class ContratoSchema(BaseModel):
    empresa: str
    cnpj: str
    data_inicio: str
    data_fim: str
    valor_contrato: str
    vigencia_prazo: str  # Trecho exato/literal
    multas_moratorias: str  # Trecho exato/literal
    multas_compensatorias: str  # Trecho exato/literal
    sancoes_administrativas: str  # Trecho exato/literal
    rescisao: str  # Trecho exato/literal
```
Essa classe será enviada na configuração de `response_schema` da API do Gemini para garantir retorno JSON tipado e contendo as cláusulas literais.

