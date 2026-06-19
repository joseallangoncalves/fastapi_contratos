---
name: analisador-precos
description: >-
  Analisa planilhas de preços unitários de contratos em formato Excel (XLSX/XLSM/CSV) 
  ou PDF, convertendo os dados para Markdown de forma otimizada para processamento rápido.
  Use esta skill quando o usuário mencionar planilha de preços, orçamento, valores unitários,
  análise de custos, extracting price data from contracts, excel de preços, ou quando precisar
  converter tabelas de preços para markdown.
compatibility:
  - xlsx
  - pdf
---

# Analisador de Preços Unitários

## Objetivo

Analisar planilhas de preços unitários de contratos (Excel ou PDF) e converter os dados
para Markdown de forma otimizada, priorizando velocidade de processamento.

## Fluxo de Trabalho Otimizado

### 1. Identificação do Tipo de Arquivo

Ao receber a solicitação do usuário:

- **Se extensão for .xlsx, .xlsm ou .csv**: Usar skill xlsx (mais rápida)
- **Se extensão for .pdf**: Usar skill pdf
- **Se não especificado**: Perguntar ao usuário o caminho do arquivo

### 2. Leitura Otimizada

#### Para Excel (prioritário):

1. Usar skill xlsx para abrir o arquivo
2. Identificar a aba principal com os dados de preços (geralmente "Itens", "Orçamento", ou primeira aba)
3. Ler todas as abas disponíveis para garantir cobertura completa

#### Para PDF:

1. Usar skill pdf para extrair o conteúdo
2. Identificar tabelas de preços no texto extraído
3. Converter para formato estruturado

### 3. Extração de Dados

Extrair os seguintes campos de cada item:

- Código do item
- Descrição do serviço/material
- Unidade de medida
- Quantidade
- Preço Unitário
- Preço Total (quantidade × preço unitário)

### 4. Conversão para Markdown

#### Estrutura da Tabela Principal:

```markdown
## Tabela de Preços Unitários

| Código | Descrição | Unidade | Qtd | Preço Unit. | Preço Total |
| ------ | --------- | ------- | --- | ----------- | ----------- |
| 001    | Serviço X | h       | 10  | R$ 50,00    | R$ 500,00   |
```

#### Resumo Estatístico:

```markdown
## Resumo

- **Total de Itens:** XX
- **Valor Total Geral:** R$ X.XXX,XX
- **Menor Valor Unitário:** R$ X,XX
- **Maior Valor Unitário:** R$ X.XXX,XX
- **Média de Preços:** R$ XXX,XX
```

#### Agrupamento por Categoria (se identificado):

```markdown
## Por Categoria

### Materiais

| Código | Descrição | Unidade | Qtd | Preço Unit. | Total |
| ------ | --------- | ------- | --- | ----------- | ----- |

### Mão de Obra

| Código | Descrição | Unidade | Qtd | Preço Unit. | Total |
| ------ | --------- | ------- | --- | ----------- | ----- |
```

### 5. Otimização de Processamento

#### Prioridades:

1. Ler dados diretamente do Excel (evitar PDF quando possível)
2. Processar apenas as colunas necessárias
3. Não aplicar formatação complexa desnecessária
4. Usar tabelas simples do Markdown (sem mesclagem)
5. Calcular totais automaticamente via script quando possível

#### Tratamento de Dados:

- Limpar espaços extras em células
- Normalizar separadores decimais (usar vírgula)
- Remover linhas vazias ou cabeçalhos duplicados
- Identificar e marcar itens com preço zero ou vazio

### 6. Saída

Gerar arquivo Markdown no diretório `C:\Users\elson\OneDrive\Antigravity\Grupo 3 - Gestão Contratual\.agents\skills\analisador-precos\output\`:

- Nome: `[Oportunidade]_precos.md`

### 7. Resumo para o Usuário

Apresentar:

- Total de itens processados
- Valor total geral
- Quantidade de categorias identificadas (se aplicável)
- Localização do arquivo Markdown gerado

## Exemplos de Uso

**Entrada 1:**
"Converta a planilha de preços C:\Orçamento\Itens_2024.xlsx para markdown"

**Entrada 2:**
"Preciso analisar o orçamento do contrato que está em PDF: C:\Docs\Orçamento_Contrato.pdf"

**Resposta esperada:**
[Leitura do arquivo, extração de dados, geração do markdown, entrega do resumo]

## Notas Importantes

- Sempre priorizar formato Excel sobre PDF para melhor performance
- Identificar e destacar itens com valores atypicals (muito altos ou muito baixos)
- Detectar se há mais de uma aba com dados relevantes
- Em caso de planilha corrompida ou PDF com texto não extraível, informar ao usuário
- Verificar se há linhas de totals/subtotais e marcá-las claramente
