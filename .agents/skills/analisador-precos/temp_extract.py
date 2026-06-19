import pandas as pd
import os

xlsx = pd.ExcelFile(r'C:\Users\elson\OneDrive\Documentos\Cursos\Pós graduação - Sistemas e Agentes Inteligentes\ePrompt\Contratos\7004259206\03-Adendo C-Anexo 2-PPU - NPI - Rev. C.xlsx')

# === SERVIÇOS ===
df_serv = pd.read_excel(xlsx, sheet_name='Anexo2-Serviços', header=6)
df_serv = df_serv[df_serv['ITEM'].notna()].copy()

servicos_data = []
for _, row in df_serv.iterrows():
    item = str(row['ITEM'])
    if '.' in item:
        desc = str(row['DESCRIÇÃO DOS SERVIÇOS']) if pd.notna(row['DESCRIÇÃO DOS SERVIÇOS']) else ''
        uni = str(row['UNIDADE']) if pd.notna(row['UNIDADE']) else '-'
        qtd = row['QUANTIDADE'] if pd.notna(row['QUANTIDADE']) else 0
        servicos_data.append({
            'Codigo': item,
            'Descricao': desc,
            'Unidade': uni,
            'Qtd': int(qtd),
            'PrecoUnit': 0.0,
            'PrecoTotal': 0.0
        })

# === BENS ===
df_bens = pd.read_excel(xlsx, sheet_name='Anexo 2A-Bens', header=12)
mask = pd.to_numeric(df_bens.iloc[:,1], errors='coerce').notna()
df_bens = df_bens[mask].copy()

# Use iloc for column positions
# Col 4 = Descrição Completa, Col 6 = Unidade, Col 12 = Preço Unitário
bens_data = []
for _, row in df_bens.iterrows():
    num_item = int(row.iloc[1])
    desc = str(row.iloc[4]) if pd.notna(row.iloc[4]) else str(row.iloc[3])
    uni = str(row.iloc[6]) if pd.notna(row.iloc[6]) else '-'
    qtd = int(row.iloc[5]) if pd.notna(row.iloc[5]) else 0
    precounit = row.iloc[12] if pd.notna(row.iloc[12]) else 0
    bens_data.append({
        'Codigo': num_item,
        'Descricao': desc,
        'Unidade': uni,
        'Qtd': qtd,
        'PrecoUnit': float(precounit),
        'PrecoTotal': float(precounit) * qtd
    })

# Output markdown
output_dir = r'C:\Users\elson\OneDrive\Antigravity\Grupo 3 - Gestão Contratual\.agents\skills\analisador-precos\output'
os.makedirs(output_dir, exist_ok=True)

md_content = f'''# Planilha de Preços Unitários - Oportunidade 7004259206

## Informações do Contrato

- **Oportunidade:** 7004259206
- **Objeto:** MULTISSERVIÇOS DE LIMPEZA, CONSERVAÇÃO, MANUTENÇÃO DE ÁREAS VERDES, CONTROLE DE PRAGAS E SERVIÇOS DE COPA
- **Arquivo:** 03-Adendo C-Anexo 2-PPU - NPI - Rev. C.xlsx

---

## 1. Serviços ({len(servicos_data)} itens)

| Código | Descrição | Unidade | Qtd | Preço Unit. | Preço Total |
| ------ | --------- | ------- | --- | ----------- | ----------- |
'''

for s in servicos_data:
    md_content += f"| {s['Codigo']} | {s['Descricao']} | {s['Unidade']} | {s['Qtd']} | R$ {s['PrecoUnit']:.2f} | R$ {s['PrecoTotal']:.2f} |\n"

total_serv = sum(s['PrecoTotal'] for s in servicos_data)
md_content += f"\n**Subtotal Serviços:** R$ {total_serv:,.2f}\n"

md_content += f'''

---

## 2. Bens ({len(bens_data)} itens)

| Código | Descrição | Unidade | Qtd | Preço Unit. | Preço Total |
| ------ | --------- | ------- | --- | ----------- | ----------- |
'''

for b in bens_data:
    md_content += f"| {b['Codigo']} | {b['Descricao']} | {b['Unidade']} | {b['Qtd']} | R$ {b['PrecoUnit']:.2f} | R$ {b['PrecoTotal']:.2f} |\n"

total_bens = sum(b['PrecoTotal'] for b in bens_data)
md_content += f"\n**Subtotal Bens:** R$ {total_bens:,.2f}\n"

md_content += f'''

---

## Resumo Estatístico

- **Total de Itens (Serviços):** {len(servicos_data)}
- **Total de Itens (Bens):** {len(bens_data)}
- **Total de Itens Geral:** {len(servicos_data) + len(bens_data)}
- **Valor Total Serviços:** R$ {total_serv:,.2f}
- **Valor Total Bens:** R$ {total_bens:,.2f}
- **Valor Total Geral:** R$ {total_serv + total_bens:,.2f}

> **Nota:** Os preços unitários dos serviços e bens estão com valor R$ 0,00 pois esta planilha é um modelo para preenchimento pelo fornecedor (PPU - Proposta de Preço Unitário).
'''

output_path = os.path.join(output_dir, '7004259206_precos.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Arquivo gerado: {output_path}")
print(f"Total serviços: {len(servicos_data)}, Total bens: {len(bens_data)}")
print(f"Valor total geral: R$ {total_serv + total_bens:,.2f}")