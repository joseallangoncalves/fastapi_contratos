# Documento Inicial - Trabalho Final de APIs para IA

Este documento detalha o escopo e o planejamento para o Trabalho Final da disciplina de Construção de APIs para Inteligência Artificial, conforme solicitado pelo professor Rogério Rodrigues Carvalho.

O objetivo deste projeto é construir uma API funcional em **FastAPI** que encapsule os nossos "Agentes" (skills) de gestão contratual existentes, transformando-os em endpoints (serviços) reais.

---

## 1. Escopo do Projeto

A API disponibiliza endpoints que utilizam LLM para realizar tarefas de análise e extração de dados a partir de documentos (PDFs). As "skills" existentes no repositório (`analisador-contratual`, `ingestao-metadados` e `reconhecimento-estratificacao`) foram expostas como serviços RESTful.

Isso cumpre o requisito principal do trabalho:
> "Desenvolver uma API funcional que disponibilize pelo menos dois serviços (endpoints) de Inteligência Artificial (IA)..."

### Endpoints Organizados e Sequenciados (Ordem no Swagger)

Todos os endpoints estão agrupados sob a tag `"Análise de Contratos (IA)"` e ordenados de forma lógica por ciclos de vida:

1. **`POST /api/v1/contratos/reconhecimento-estratificacao`**
   - **Objetivo**: Mapear os intervalos exatos de páginas de cada seção do contrato (SMS, PPU, ICJ, etc.), classificar o tipo predominante de conteúdo de cada página e extrair o número do contrato.
   - **Requisitos de Arquivo**: Formato PDF (.pdf) e tamanho máximo de 50MB.
2. **`POST /api/v1/contratos/ingestao-metadados`**
   - **Objetivo**: Extrair e persistir informações cadastrais do contrato.
   - **Regra**: Não persiste o corpo do ICJ brutos, apenas os atributos cadastrais.
   - **Prazos**: Prazos de vigência e prazo de execução extraídos obrigatoriamente em **dias** (inteiro positivo).
   - **Requisitos de Arquivo**: Formato PDF (.pdf) e tamanho máximo de 50MB.
3. **`POST /api/v1/contratos/analise-contratual`**
   - **Objetivo**: Extrair cláusulas de penalidades, multas (moratórias e compensatórias), sanções administrativas e condições de rescisão, além de calcular a data fim com base no prazo em dias.
   - **Prazos**: Prazo de vigência extraído obrigatoriamente em **dias** (inteiro positivo).
   - **Requisitos de Arquivo**: Formato PDF (.pdf) e tamanho máximo de 50MB.
4. **`GET /api/v1/contratos/reconhecimento-estratificacao`**
   - **Objetivo**: Listar as estratificações de páginas persistidas. Permite busca inteligente por `numero_contrato`.
5. **`GET /api/v1/contratos/reconhecimento-estratificacao/{id}`**
   - **Objetivo**: Obter detalhes de uma estratificação específica pelo ID numérico único.
6. **`GET /api/v1/contratos/ingestao-metadados`**
   - **Objetivo**: Listar metadados cadastrais. Permite busca inteligente por `numero_contrato` ou `contratada`.
7. **`GET /api/v1/contratos/ingestao-metadados/{id}`**
   - **Objetivo**: Obter os detalhes cadastrais de um registro específico pelo ID.
8. **`GET /api/v1/contratos/analises`**
   - **Objetivo**: Listar análises de cláusulas. Permite busca inteligente por `numero_contrato`, `cnpj` ou `empresa`.
9. **`GET /api/v1/contratos/analises/{id}`**
   - **Objetivo**: Obter os detalhes de uma análise contratual específica pelo ID.
10. **`PATCH /api/v1/contratos/analises/{id}`**
    - **Objetivo**: Atualizar de forma parcial dados de análises contratuais existentes.
11. **`DELETE /api/v1/contratos/analises/{id}`**
    - **Objetivo**: Remover uma análise contratual do banco de dados (requer parâmetro de confirmação `confirm=true`).

---

## 2. Atendimento aos Requisitos Obrigatórios

Para obtermos a nota máxima e cumprirmos o que foi passado no PDF, as seguintes características foram integradas ao projeto:

* **[x] Serviço de IA Diferenciado**: Utilização de IA Generativa integrada aos agentes locais especialistas de gestão contratual.
* **[x] Prazos Uniformes em Dias**: Todos os prazos do projeto (vigência de contrato, prazo de vigência nas análises e prazos de execução) são extraídos, armazenados e validados estritamente na unidade de **dias** (inteiros positivos), permitindo precisão absoluta (ex: contratos de 1115 dias).
* **[x] Validação de Dados de Entrada**:
  - Restrição robusta de uploads: arquivos devem ser obrigatoriamente do formato PDF (`.pdf`) e respeitar o tamanho limite de **50MB** por upload.
  - Validação de filtros de busca: o preenchimento de filtros de `numero_contrato` ou `cnpj` nas rotas GET de listagem obriga que o dado contenha **exatamente 14 dígitos numéricos** (com ou sem pontuação). Em caso de inconformidade, retorna o status HTTP **`400 Bad Request`** com mensagem explicativa.
  - Validação estrita de tipos por path parameter (ex: buscar `/analises/abc` gera erro automático **`422 Unprocessable Entity`** do FastAPI/Pydantic).
* **[x] Busca Inteligente e Sanitização**:
  - Filtros de busca por CNPJ e Número de Contrato ignoram automaticamente pontuações (`.`, `-`, `/`), espaços e o prefixo `ICJ` tanto no termo digitado quanto na coluna correspondente do banco de dados para evitar incompatibilidades de busca.
* **[x] Tratamento de Erros**:
  - Respostas amigáveis em caso de arquivo corrompido ou inválido (HTTP 400).
  - Tratamento de falhas de comunicação com a IA (HTTP 502).
  - Retorno HTTP **`404 Not Found`** com mensagem clara quando um ID específico não é localizado.
* **[x] Logs**:
  - Sistema de `logging` detalhado registrando acessos aos endpoints, tempos de processamento da IA e possíveis exceções ocorridas.
* **[x] Segurança**:
  - Todos os endpoints sob `/api/v1/contratos` exigem autenticação via token Bearer válido, integrados com o controle de segurança.
* **[x] Documentação Enriquecida**:
  - Todas as rotas, parâmetros de entrada (Query, Path) e schemas de payloads de entrada/saída contêm descrições detalhadas em português e exemplos preenchidos reais no Swagger para facilitar o uso.
  - Divisão explícita de POSTs agrupados primeiro, seguidos por GETs de listagem, GETs de busca de IDs específicos e finalizando com operações de alteração/exclusão (PATCH/DELETE).

---

## 3. Próximos Passos (Plano de Ação)

1. **Testes de Integração Completos**
   - Validar o upload de contratos reais nas rotas POST e confirmar a persistência dos dados (incluindo o prazo calculado em dias).
   - Validar as buscas no Swagger utilizando termos de contratos sem formatação e verificar as respostas de erro de tamanho do filtro.
2. **Entrega da Disciplina**
   - Gravar o vídeo demonstrando o Swagger e a chamada dos endpoints.
   - Fornecer o arquivo `README.md` atualizado com as instruções de instalação e execução rápida.

