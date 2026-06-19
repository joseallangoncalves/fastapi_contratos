---
name: analisador-consumo
description: |
  Analisa arquivos Excel de consumo de contratos de manutenção industrial e converte para formato Markdown.
  Use esta skill quando o usuário mencionar: "analisar consumo", "converter consumo para MD",
  "extrair dados de consumo", "relatório de consumo", "consumo contrato", "_follow-up de consumo".
  A skill processa arquivos Excel (.xlsx, .xlsm) contendo dados de consumo de contratos,
  extrai as informações de quantidade prevista, realizada e saldo, e gera um relatório
  estruturado em Markdown salvo no diretório output da skill.
---

# Skill: Analisador de Consumo

## Objetivo

Analisar arquivos Excel de consumo de contratos de manutenção industrial, extrair os dados de quantidade prevista, realizada e saldo, e converter para formato Markdown com estrutura organizada por categorias.

## Fluxo de Trabalho

### 1. Identificação do Arquivo

O usuário deve fornecer o caminho do arquivo Excel de consumo (.xlsx ou .xlsm).

### 2. Leitura do Excel

1. Usar a skill xlsx para abrir o arquivo
2. Identificar a aba principal com os dados de consumo (geralmente "Página1" ou primeira aba)
3. Ler todas as linhas para extrair informações de cada item

### 3. Extração de Dados

Para cada item do contrato, extrair:

- Código do item
- Descrição do serviço/material
- Valor Unitário
- Quantidade Prevista
- Quantidade Realizada (FRS)
- Saldo de Quantidade (LS)
- Valor Previsto
- Valor Realizado (FRS)
- Saldo de Valor (FRS)

### 4. Conversão para Markdown

Estrutura do relatório:

```markdown
# Relatório de Consumo - [Nome do Contrato]

## Resumo Geral

- **Contrato:** [Número]
- **Objeto:** [Descrição]
- **Valor Previsto Total:** R$ X.XXX.XXX,XX
- **Valor Realizado (FRS):** R$ X.XXX.XXX,XX
- **Saldo Valor (FRS):** R$ X.XXX.XXX,XX

---

## Tabela de Itens de Consumo

| Código | Descrição | Valor Unit. | Qtd Prevista | Qtd Realizada | Saldo Qtd | Valor Previsto | Valor Realizado | Saldo Valor |
| ------ | --------- | ----------- | ------------ | ------------- | --------- | -------------- | --------------- | ----------- |
```

### 5. Agrupamento por Categoria

Agrupar os itens por categorias (A, B, C, D, E) conforme a estrutura do contrato:

- A - Serviços de Rotina
- B - Equipamentos Dinâmicos
- C - Elétrica e Instrumentação
- D - Caldeiraria
- E - Disponibilização de Recursos

### 6. Resumo Estatístico

Incluir resumo com:

- Total de itens
- Valor total previsto
- Valor total realizado
- Percentual de execução
- Itens com maior execução
- Itens sem execução

### 7. Saída

Salvar o arquivo Markdown no diretório `C:\Users\elson\OneDrive\Antigravity\Grupo 3 - Gestão Contratual\.agents\skills\analisador-consumo\output\`:

- Nome: `[Oportunidade]_consumo.md`

## Exemplo de Uso

**Entrada:**

```
Analise o consumo do arquivo C:\Users\elson\Documentos\contratos\7004166210\Consumo - Lote 1.xlsx
```

**Saída:**

- Arquivo Markdown com relatório de consumo estruturado
- Salvo em: `...\analisador-consumo\output\7004166210_consumo.md`

## Notas Importantes

- O arquivo Excel pode ter formatação específica da Petrobras
- Identificar linhas de cabeçalho e totais
- Tratar valores numéricos com separadores decimais corretos
- Preservar acentuação e caracteres especiais
- Gerar resumo executivo com estatísticas relevantes
