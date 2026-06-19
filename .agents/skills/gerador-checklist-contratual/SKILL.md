---
name: gerador-checklist-contratual
description: Gera checklists de verificação para fiscalização de contratos. Use esta skill sempre que o usuário precisar criar listas de verificação para contratos, incluindo casos onde menciona "criar checklist", "lista de verificação", "checklist de contrato", "verificação de contrato", "recebimento provisório", "recebimento definitivo", ou quando precisar gerar listas de conformance para fiscalização de contratos.
---

## Descrição

Esta skill gera checklists de verificação para fiscalização de contratos, organizados por categoria (financeiro, técnico, legal).

## Input

- Pasta do contrato ou informações sobre o contrato
- Fase do contrato para gerar checklist

## Passos

1. **Identificar a fase do contrato**
   - Pergunte ao usuário qual fase: Execução
   - Cada fase tem requisitos específicos

2. **Gerar checklist conforme fase**

### Checklist de Execução

- Verificação inicial de documentos
- Acompanhamento de cronograma
- Verificação de pagamentos
- Controle de alterações

3. **Gerar formato markdown**

   ```markdown
   # Checklist de Verificação - [FASE]

   ## Contrato: [NOME]

   Data de geração: [DATA]

   ## Instruções

   Marque ✅ quando conforme, ❌ quando não conforme, ou N/A quando não se aplica.

   ---

   ### 1. Documentação Financeira

   | Item                                     | Status | Observações |
   | ---------------------------------------- | ------ | ----------- |
   | Faturas presentadas conforme contrato    | ☐      |             |
   | Valores corretos conforme medição        | ☐      |             |
   | Impostos retidos corretamente            | ☐      |             |
   | Boletos/pagamentos properly documentados | ☐      |             |

   ### 2. Documentação Técnica

   | Item                                   | Status | Observações |
   | -------------------------------------- | ------ | ----------- |
   | Relatórios técnicos entregues          | ☐      |             |
   | Cronograma seguito                     | ☐      |             |
   | Marcos de entrega atingidos            | ☐      |             |
   | Documentação as-built quando aplicável | ☐      |             |

   ### 3. Documentação Legal

   | Item                              | Status | Observações |
   | --------------------------------- | ------ | ----------- |
   | Certidões válidas                 | ☐      |             |
   | Alvarás em dia                    | ☐      |             |
   | Conformidade ambiental            | ☐      |             |
   | Registro da obra quando aplicável | ☐      |             |

   ### 4. Verificações Gerais

   | Item                               | Status | Observações |
   | ---------------------------------- | ------ | ----------- |
   | Contrato acessível para referência | ☐      |             |
   | Registro de ocorrências atualizado | ☐      |             |
   | Comunicações documentadas          | ☐      |             |

   ---

   ## Resumo

   Total de itens: _
   Conformes: _
   Não conformes: _
   Não aplicáveis: _

   ## Pendências Identificadas

   -

   ## Assinaturas

   | Função              | Nome | Data | Assinatura |
   | ------------------- | ---- | ---- | ---------- |
   | Fiscal do contrato  |      |      |            |
   | Responsável técnico |      |      |            |
   ```

4. **Salvar o checklist**
   - Salve como `[OP]_checklist_[fase].md` na pasta output da skill, se não existar a pasta output, basta criar

## Categorias

O checklist inclui 4 categorias principais:

1. **Financeira** - Faturas, pagamentos, valores
2. **Técnica** - Execução, cronogramas, relatórios
3. **Legal** - Certidões, alvarás, compliance
4. **Geral** - Organização, documentação, registros

## Notas

- O checklist é interativo (pode ser preenchido manualmente depois)
- Inclui espaço para observações em cada item
- Tem área para assinaturas
- Calcula resumo automaticamente
- Permite identificar pendências para follow-up
