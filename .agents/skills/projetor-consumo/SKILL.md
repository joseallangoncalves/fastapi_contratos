---
name: projetor-consumo
description: |
  Realiza análise de projeção de consumo de contratos. Use quando o usuário mencionar: "projeção de consumo", "análise de tendência", "consumo estimado", "projeção contratual", "forecast de consumo", "linhas críticas", "consumo vs contrato", "excesso de consumo", "subutilização". A skill lê dados de consumo de um arquivo Markdown (gerado pelo analisador-consumo), automaticamente identifica o período dos dados e calcula a projeção considerando o tempo real decorrido desde o início do contrato.
---

# Skill: Projetor de Consumo

## Objetivo

Realizar análise de projeção de consumo de contratos de manutenção industrial, identificando itens críticos que estão com risco de extrapolação ou subutilização do contrato.

## Como Usar

Ao invocar esta skill, forneça:

1. **Caminho do arquivo Markdown** com dados de consumo (gerado pelo analisador-consumo)
2. **Data de Início** do contrato (DD/MM/AAAA) - OBRIGATÓRIO
3. **Data de Término** do contrato (DD/MM/AAAA) - OBRIGATÓRIO
4. **Vigência** em meses - OBRIGATÓRIO

### Execução via Python

```bash
python scripts/projetor.py <arquivo_markdown> <inicio> <termino> <vigencia>
```

Exemplo:

```bash
python scripts/projetor.py "C:\Docs\7004166210_consumo.md" "21/02/2024" "19/04/2028" "48"
```

Parâmetros:
- `<arquivo_markdown>`: Caminho do arquivo MD gerado pelo analisador-consumo
- `<inicio>`: Data de início do contrato (DD/MM/AAAA)
- `<termino>`: Data de término do contrato (DD/MM/AAAA)
- `<vigencia>`: Vigência total em meses (número)

## Formato do Arquivo de Entrada

O arquivo Markdown deve seguir este formato (gerado pelo analisador-consumo):

```markdown
# Consumo Histórico - Contrato XXXXXX

## Parâmetros do Contrato

- Oportunidade: 7004166210
- Contrato: 7004166210 - Lote 1
- Início: 21/02/2024
- Término: 19/04/2028
- Vigência: 48 meses
- Valor Total Contratado: R$ 81.043.956,73

---

## Histórico de Consumo

| Código | Descrição | Unidade | Qtd Contratada | Abr/2024 | Mai/2024 | ... | Fev/2026 |
|--------|-----------|---------|----------------|----------|----------|-----|----------|
| 20 | A1 Serviço Mensal | UN | 48 | 1.600 | 0.988 | ... | 0.918 |
```

### Regras do Formato

- A tabela deve ter colunas: Código, Descrição, Unidade, Qtd Contratada, e colunas de meses
- As colunas de mês devem seguir o formato: Mês/Ano (ex: Abr/2024, Mai/2024)
- Os valores de consumo usam vírgula como separador decimal (ex: 1.600, 0.918)

## Lógica de Projeção

### Cálculo de Meses Passados

A skill calcula automaticamente o número de meses transcurridos desde o início do contrato até o último mês com dados históricos:

```
Meses Passados = (Mês do último dado - Mês de início do contrato) + 1
Meses Restantes = Vigência do contrato - Meses Passados
```

### Opção 1: Histórico Total

Calcula a média mensal usando todos os meses do histórico disponível:

```
Média Mensal = (Soma de todos os meses) / (Número total de meses no histórico)
Projeção Futura = Média Mensal × Meses Restantes
```

### Opção 2: Últimos 90 Dias (3 meses)

Calcula a média dos últimos 3 meses do histórico:

```
Média Mensal = (Mês1 + Mês2 + Mês3) / 3
Projeção Futura = Média Mensal × Meses Restantes
```

### Classificação de Status

O status é calculado baseado na **projeção de consumo no término do contrato**:

| Status          | Condição                    | Cor no Relatório |
| --------------- | --------------------------- | ---------------- |
| 🔴 Crítico      | Projeção > 100%             | Vermelho         |
| 🟠 Risco Alto   | Projeção entre 95-100%      | Laranja          |
| 🟡 Atenção      | Projeção entre 85-95%       | Amarelo          |
| 🟢 Normal       | Projeção entre 50-85%       | Verde            |
| 🔵 Subutilizado | Projeção ≤ 50%              | Azul             |

**Cálculo:**
- `% Atingido` = Consumo total realizado até o momento / Qtd Contratada × 100
- `% Projeção` = (Consumo total + Média mensal × Meses restantes) / Qtd Contratada × 100
- Média mensal = Consumo total / Meses transcorridos

## Saída

A skill gera um arquivo HTML com:

- Cabeçalho com informações do contrato (início, término, vigência, método)
- Cards de resumo (itens críticos, risco alto, subutilizados)
- Tabela detalhada com todas as métricas por item
- Legenda de cores e status

Arquivo de saída: `[diretório_do_markdown]/[Oportunidade]_projecao_consumo.html`

## Arquivos Inclusos na Skill

```
projetor-consumo/
├── SKILL.md              # Este arquivo
├── scripts/
│   └── projetor.py        # Script de processamento
└── output/                # Arquivos gerados
```

## Exemplo de Uso

**Entrada:**

```
Analise a projeção de consumo do arquivo C:\Docs\7004166210_consumo.md
```

**Resultado:**

- Relatório HTML gerado com análise completa
- Destaque visual para itens críticos (projeção > 100% do saldo)
- Exibe consumo total, média mensal, projeção futura, % atingido, % projeção
- Classificação automática de status

## Notas Importantes

- O arquivo Markdown de entrada é gerado pela skill `analisador-consumo`
- A skill automaticamente identifica o período dos dados históricos e calcula os meses transcurridos
- Itens com consumo zero em todos os meses são ignorados
- As datas de início/término e vigência são lidas dos parâmetros do arquivo Markdown
- O parsing suporta números com vírgula como separador decimal
