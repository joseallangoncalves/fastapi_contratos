---
name: analisador-sms
description: >-
  Analisa documentação de SMS (Segurança, Saúde e Meio Ambiente) de contratos, 
  extraindo os principais pontos relevantes para a Contratada e para a Contratante.
  Use esta skill quando o usuário mencionar análise de SMS, requisitos de segurança,
  documento de SMS, análise de contrato SMS, extracting safety requirements from contracts,
  ou quando precisar analisar documentos PDF de requisitos de SMS em contratos.
compatibility:
  - pdf
---

# Analisador de SMS

## Objetivo

Analisar documentos PDF de SMS (Segurança, Saúde e Meio Ambiente) de contratos e extrair
os principais pontos relevantes para a Contratada e para a Contratante, gerando relatórios
em múltiplos formatos (TXT, PDF e HTML).

## Fluxo de Trabalho

### 1. Solicitação do Arquivo

Caso o usuário não tenha fornecido o caminho do arquivo PDF, solicitar educadamente o diretório
ou nome do arquivo contendo a documentação de SMS.

### 2. Leitura do PDF

Utilizar a skill pdf para extrair o conteúdo textual do documento PDF de SMS.

### 3. Análise Categorizada

Analisar o conteúdo extraído e categorizar as informações em:

#### Para a Contratada:

- EPIs e equipamentos de proteção exigidos
- Certificações e treinamentos obrigatórios
- Procedimentos de emergência e primeiros socorros
- Requisitos ambientais e gestão de resíduos
- Responsabilidades específicas de segurança
- Obrigações de manutenção de registros
- Requisitos de comunicação de incidentes

#### Para a Contratante:

- Obrigações de fiscalização e monitoramento
- Requisitos de relatórios e documentação
- Periodicidade de auditorias e inspeções
- Recursos e infraestrutura disponibilizados
- Responsabilidades pela medicina do trabalho
- Requisitos de comunicação e notificação

#### Categorias de SMS:

1. **Segurança (S)**: EPIs, procedimentos, treinamentos, incidentes, investigação de acidentes
2. **Saúde (S)**: Medicina ocupacional, exames admissionais/periódicos, ergonomia
3. **Meio Ambiente (A)**: Licenças, gestão de resíduos, impactos ambientais, emergências ambientais

### 4. Estrutura do Relatório

O relatório deve seguir esta estrutura:

```
# RELATÓRIO DE ANÁLISE DE SMS

## 1. Informações Gerais
- Nome do Documento
- Data de Extração
- Número do Contrato (se identificado)

## 2. Resumo Executivo
Breve descrição do escopo de SMS coberto pelo documento.

## 3. Pontos Relevantes para a Contratada

### 3.1 EPIs e Equipamentos de Proteção
[Listagem dos EPIs exigidos]

### 3.2 Certificações e Treinamentos
[Listagem de certificações e treinamentos obrigatórios]

### 3.3 Procedimentos de Emergência
[Descrição dos procedimentos exigidos]

### 3.4 Requisitos Ambientais
[Requisitos de gestão ambiental]

### 3.5 Obrigações de Registro e Comunicação
[Requisitos de documentação e comunicação de incidentes]

## 4. Pontos Relevantes para a Contratante

### 4.1 Obrigações de Fiscalização
[Requisitos de monitoramento e fiscalização]

### 4.2 Requisitos de Comunicação
[Obrigações de notificação e relatórios]

### 4.3 Responsabilidades por Medicina do Trabalho
[Obrigações relacionadas à saúde ocupacional]

## 5. Tabela de Responsabilidades Cruzadas
| Requisito | Contratada | Contratante |
|-----------|------------|-------------|
| [Item]   | [X]        | [X]         |

## 6. Riscos e Pontos de Atenção
[Destaque para pontos críticos identificados]

## 7. Recomendações
Sugestões para a Contratada e Contratante.
```

### 5. Geração dos Arquivos de Saída

Após a análise, gerar os seguintes arquivos no diretório `C:\Users\elson\OneDrive\Antigravity\Grupo 3 - Gestão Contratual\.agents\skills\analisador-sms\output\`:

1. **TXT**: `[Oportunidade]_SMS_analise.txt` - Relatório completo em texto
2. **PDF**: `[Oportunidade]_SMS_analise.pdf` - Relatório formatado em PDF
3. **HTML**: `[Oportunidade]_SMS_analise.html` - Relatório em formato HTML com estilo

### 6. Entrega do Resultado

Apresentar ao usuário um resumo dos principais pontos encontrados, com destaque para:

- Quantidade de EPIs identificados
- Quantidade de treinamentos/certificações exigidas
- Requisitos ambientais críticos
- Pontos de atenção para a Contratada
- Pontos de atenção para a Contratante

Indicar a localização dos arquivos gerados.

## Exemplos de Uso

**Entrada do usuário:**
"Preciso analisar o documento de SMS do contrato 123/2024 que está em C:\Users\Documents\SMS_Contrato.pdf"

**Resposta esperada:**
[Leitura do PDF, análise categorizada, geração dos relatórios e entrega do resumo]

## Notas Importantes

- Ao identificar números de contrato ou oportunidades, registrá-los no relatório
- Destacar pontos que possam gerar penalidades ou multas se não cumpridos
- Identificar prazos e periodicidades mencionadas
- Observar se há referência a normas específicas (NRs, ISO, etc.)
- Em caso de texto ilegível ou corrompido, informar ao usuário e sugerir nova versão do documento
