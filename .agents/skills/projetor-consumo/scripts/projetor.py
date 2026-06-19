import re
import sys
from datetime import datetime
from pathlib import Path

meses_map = {
    'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6,
    'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12
}

def parse_markdown_consumption(file_path):
    """Parse markdown file with consumption data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    params = {}
    items = []
    
    lines = content.split('\n')
    
    param_pattern = r'^- (.+?): (.+)$'
    for line in lines:
        match = re.match(param_pattern, line.strip())
        if match:
            key, value = match.groups()
            params[key.strip()] = value.strip()
    
    table_started = False
    header_cols = []
    month_columns = []
    
    for i, line in enumerate(lines):
        if '| Código |' in line and '| Descrição |' in line:
            table_started = True
            header_cols = [c.strip() for c in line.split('|') if c.strip()]
            month_columns = [c.strip() for c in line.split('|') if c.strip() and '/' in c]
            continue
        
        if table_started and line.startswith('|') and '---' not in line:
            if '|' in line:
                cols = [c.strip() for c in line.split('|') if c.strip()]
                
                if len(cols) >= 6 and cols[0]:
                    codigo = cols[0].split(' ')[0] if cols[0] else ''
                    if codigo.isdigit():
                        qtd_prevista = 0
                        qtd_realizada = 0
                        valor_previsto = 0
                        valor_realizado = 0
                        
                        try:
                            qtd_prevista = float(cols[3].replace('.', '').replace(',', '.')) if len(cols) > 3 and cols[3] else 0
                        except:
                            qtd_prevista = 0
                        
                        try:
                            qtd_realizada = float(cols[4].replace('.', '').replace(',', '.')) if len(cols) > 4 and cols[4] else 0
                        except:
                            qtd_realizada = 0
                        
                        if len(cols) > 6:
                            try:
                                valor_previsto = float(cols[6].replace('R$', '').replace('.', '').replace(',', '.').strip()) if cols[6] else 0
                            except:
                                valor_previsto = 0
                        
                        if len(cols) > 7:
                            try:
                                valor_realizado = float(cols[7].replace('R$', '').replace('.', '').replace(',', '.').strip()) if cols[7] else 0
                            except:
                                valor_realizado = 0
                        
                        qtd_contratada = qtd_prevista
                        
                        descricao = ' '.join(cols[0:2]) if len(cols) > 1 else cols[0]
                        
                        item = {
                            'codigo': codigo,
                            'descricao': descricao,
                            'unidade': cols[2] if len(cols) > 2 else '',
                            'qtd_contratada': qtd_contratada,
                            'consumo_mensal': [],
                            'qtd_prevista': qtd_prevista,
                            'qtd_realizada': qtd_realizada,
                            'valor_previsto': valor_previsto,
                            'valor_realizado': valor_realizado
                        }
                        
                        if qtd_prevista > 0:
                            items.append(item)
    
    for line in lines:
        if '**Contrato**' in line or '| Contrato |' in line:
            match = re.search(r'\*\*Contrato\*\*.*?(\d{10})', line)
            if match:
                params['Oportunidade'] = match.group(1)
        if '**Valor Previsto Total**' in line:
            match = re.search(r'R\$\s*([\d\.]+,\d+)', line)
            if match:
                params['Valor Total Contratado'] = match.group(1)
    
    return params, items, month_columns

def calculate_projection(items, method='total', vigencia_meses=24, month_columns=None, inicio_contrato=None, vigencia_str=''):
    """Calculate consumption projection."""
    from datetime import datetime
    
    meses_passados = 0
    
    if inicio_contrato:
        try:
            inicio_dt = datetime.strptime(inicio_contrato, '%d/%m/%Y')
            hoje = datetime.now()
            meses_passados = (hoje.year - inicio_dt.year) * 12 + hoje.month - inicio_dt.month + 1
            meses_passados = max(0, meses_passados)
        except:
            meses_passados = 6
    elif vigencia_str:
        try:
            meses_passados = int(vigencia_str.replace('meses', '').strip()) // 2
        except:
            meses_passados = 6
    else:
        meses_passados = 6
    
    if meses_passados == 0:
        meses_passados = 6
    
    meses_futuros = max(0, vigencia_meses - meses_passados)
    
    results = []
    
    for item in items:
        qtd_prevista = item.get('qtd_prevista', 0) or 0
        qtd_realizada = item.get('qtd_realizada', 0) or 0
        
        qtd_contratada = item.get('qtd_contratada', 0)
        if qtd_contratada == 0:
            qtd_contratada = qtd_prevista
        
        if qtd_contratada <= 0 or qtd_realizada <= 0:
            continue
        
        consumo_total = qtd_realizada
        consumo_restante = qtd_contratada - consumo_total
        
        if meses_passados > 0:
            media_mensal = consumo_total / meses_passados
        else:
            media_mensal = 0
        
        projecao_futura = media_mensal * meses_futuros
        
        percentual_atingido = (consumo_total / qtd_contratada * 100) if qtd_contratada > 0 else 0
        
        projecao_total = consumo_total + projecao_futura
        percentual_projecao = (projecao_total / qtd_contratada * 100) if qtd_contratada > 0 else 0
        
        if percentual_projecao > 100:
            status = 'crítico'
            classe = 'critico'
        elif percentual_projecao > 95:
            status = 'risco-alto'
            classe = 'risco-alto'
        elif percentual_projecao > 85:
            status = 'atenção'
            classe = 'atencao'
        elif percentual_projecao > 50:
            status = 'normal'
            classe = 'normal'
        else:
            status = 'subutilizado'
            classe = 'subutilizado'
        
        percentual = percentual_projecao
        
        resultados = {
            'codigo': item['codigo'],
            'descricao': item['descricao'],
            'unidade': item['unidade'],
            'qtd_contratada': qtd_contratada,
            'consumo_total': consumo_total,
            'consumo_restante': consumo_restante,
            'percentual_atingido': percentual_atingido,
            'media_mensal': media_mensal,
            'projecao_futura': projecao_futura,
            'projecao_total': consumo_total + projecao_futura,
            'percentual': percentual,
            'status': status,
            'classe': classe,
            'meses_passados': meses_passados,
            'meses_futuros': meses_futuros,
            'percentual_projecao': percentual_projecao
        }
        
        results.append(resultados)
    
    return results

def generate_html(params, results, method):
    """Generate HTML report."""
    
    critic_count = sum(1 for r in results if r['status'] == 'crítico')
    risco_alto_count = sum(1 for r in results if r['status'] == 'risco-alto')
    atencao_count = sum(1 for r in results if r['status'] == 'atenção')
    normal_count = sum(1 for r in results if r['status'] == 'normal')
    subutilizado_count = sum(1 for r in results if r['status'] == 'subutilizado')
    
    method_text = "Histórico Total" if method == 'total' else "Últimos 90 Dias (3 meses)"
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Projeção de Consumo - {params.get('Oportunidade', 'N/A')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 10px 0; font-size: 28px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 16px; }}
        .info-box {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .info-box h2 {{ margin-top: 0; color: #1e3c72; font-size: 20px; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }}
        .info-item {{ padding: 10px; background: #f8f9fa; border-radius: 5px; }}
        .info-item label {{ display: block; font-size: 12px; color: #666; }}
        .info-item value {{ display: block; font-size: 16px; font-weight: bold; color: #333; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }}
        .summary-card {{ background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary-card.critico {{ border-left: 5px solid #dc3545; }}
        .summary-card.risco {{ border-left: 5px solid #fd7e14; }}
        .summary-card.subutilizado {{ border-left: 5px solid #0d6efd; }}
        .summary-card.total {{ border-left: 5px solid #198754; }}
        .summary-card .number {{ font-size: 36px; font-weight: bold; }}
        .summary-card.critico .number {{ color: #dc3545; }}
        .summary-card.risco .number {{ color: #fd7e14; }}
        .summary-card.atencao .number {{ color: #ffc107; }}
        .summary-card.normal .number {{ color: #198754; }}
        .summary-card.subutilizado .number {{ color: #0d6efd; }}
        .summary-card.total .number {{ color: #198754; }}
        .summary-card .label {{ color: #666; font-size: 14px; }}
        .summary-card.atencao {{ border-left: 5px solid #ffc107; }}
        .summary-card.normal {{ border-left: 5px solid #198754; }}
        table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden; }}
        th {{ background: #1e3c72; color: white; padding: 15px; text-align: left; font-weight: 600; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}
        .critico {{ background-color: #ffcccc; color: #990000; font-weight: bold; }}
        .risco-alto {{ background-color: #ffe6cc; color: #995500; }}
        .atencao {{ background-color: #ffffcc; color: #666600; }}
        .normal {{ background-color: #ccffcc; color: #006600; }}
        .subutilizado {{ background-color: #cce6ff; color: #003366; }}
        .badge {{ padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; }}
        .badge-critico {{ background: #dc3545; color: white; }}
        .badge-risco {{ background: #fd7e14; color: white; }}
        .badge-atencao {{ background: #ffc107; color: #333; }}
        .badge-normal {{ background: #198754; color: white; }}
        .badge-subutilizado {{ background: #0d6efd; color: white; }}
        .footer {{ margin-top: 30px; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Análise de Projeção de Consumo</h1>
            <div class="subtitle">Contrato: {params.get('Contrato', 'N/A')} | Oportunidade: {params.get('Oportunidade', 'N/A')}</div>
        </div>
        
        <div class="info-box">
            <h2>Parâmetros do Contrato</h2>
            <div class="info-grid">
                <div class="info-item">
                    <label>Oportunidade</label>
                    <value>{params.get('Oportunidade', 'N/A')}</value>
                </div>
                <div class="info-item">
                    <label>Início</label>
                    <value>{params.get('Início', 'N/A')}</value>
                </div>
                <div class="info-item">
                    <label>Término</label>
                    <value>{params.get('Término', 'N/A')}</value>
                </div>
                <div class="info-item">
                    <label>Vigência</label>
                    <value>{params.get('Vigência', 'N/A')}</value>
                </div>
                <div class="info-item">
                    <label>Valor Contratado</label>
                    <value>{params.get('Valor Total Contratado', 'N/A')}</value>
                </div>
                <div class="info-item">
                    <label>Método de Projeção</label>
                    <value>{method_text}</value>
                </div>
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card critico">
                <div class="number">{critic_count}</div>
                <div class="label">Crítico (>100%)</div>
            </div>
            <div class="summary-card risco">
                <div class="number">{risco_alto_count}</div>
                <div class="label">Risco Alto (95-100%)</div>
            </div>
            <div class="summary-card atencao">
                <div class="number">{atencao_count}</div>
                <div class="label">Atenção (85-95%)</div>
            </div>
            <div class="summary-card normal">
                <div class="number">{normal_count}</div>
                <div class="label">Normal (50-85%)</div>
            </div>
            <div class="summary-card subutilizado">
                <div class="number">{subutilizado_count}</div>
                <div class="label">Subutilizado (≤50%)</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Descrição</th>
                    <th>Unidade</th>
                    <th>Qtd Contratada</th>
                    <th>Consumo Total</th>
                    <th>Média Mensal</th>
                    <th>Proj. Futura</th>
                    <th>% Atingido</th>
                    <th>% Projeção</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for r in results:
        badge_class = {
            'crítico': 'badge-critico',
            'risco-alto': 'badge-risco',
            'atenção': 'badge-atencao',
            'normal': 'badge-normal',
            'subutilizado': 'badge-subutilizado'
        }.get(r['status'], '')
        
        html += f"""
                <tr class="{r['classe']}">
                    <td><strong>{r['codigo']}</strong></td>
                    <td>{r['descricao'][:70]}{'...' if len(r['descricao']) > 70 else ''}</td>
                    <td>{r['unidade']}</td>
                    <td>{r['qtd_contratada']:,.2f}</td>
                    <td>{r['consumo_total']:,.2f}</td>
                    <td>{r['media_mensal']:,.2f}</td>
                    <td>{r['projecao_futura']:,.2f}</td>
                    <td>{r['percentual_atingido']:.1f}%</td>
                    <td>{r['percentual']:.1f}%</td>
                    <td><span class="badge {badge_class}">{r['status'].upper()}</span></td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>Relatório gerado automaticamente pela skill projetor-consumo</p>
            <p>Legenda: 🔴 Crítico (>100%) | 🟠 Risco Alto (95-100%) | 🟡 Atenção (85-95%) | 🟢 Normal (50-85%) | 🔵 Subutilizado (≤50%)</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Usage: python projetor.py <markdown_file> [inicio] [termino] [vigencia]")
        print("  inicio: data de início (DD/MM/AAAA)")
        print("  termino: data de término (DD/MM/AAAA)")
        print("  vigencia: vigência em meses (número)")
        sys.exit(1)
    
    file_path = sys.argv[1]
    method = 'total'
    
    inicio_contrato = sys.argv[2] if len(sys.argv) > 2 else ''
    termino_contrato = sys.argv[3] if len(sys.argv) > 3 else ''
    vigencia_str = sys.argv[4] if len(sys.argv) > 4 else ''
    
    params, items, month_columns = parse_markdown_consumption(file_path)
    
    params['Início'] = inicio_contrato
    params['Término'] = termino_contrato
    params['Vigência'] = vigencia_str
    
    vigencia_meses = 24
    
    if vigencia_str:
        try:
            vigencia_meses = int(vigencia_str)
        except:
            pass
    elif inicio_contrato and termino_contrato:
        try:
            inicio_dt = datetime.strptime(inicio_contrato, '%d/%m/%Y')
            termino_dt = datetime.strptime(termino_contrato, '%d/%m/%Y')
            delta = termino_dt - inicio_dt
            vigencia_meses = max(1, delta.days // 30)
        except:
            pass
    
    results = calculate_projection(items, method, vigencia_meses, month_columns, inicio_contrato, vigencia_str)
    html = generate_html(params, results, method)
    
    output_path = Path(file_path).parent / f"{params.get('Oportunidade', 'output')}_projecao_consumo.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Relatório gerado: {output_path}")
    print(f"Total de itens: {len(results)}")
    print(f"Itens críticos: {sum(1 for r in results if r['status'] == 'crítico')}")
    print(f"Itens risco alto: {sum(1 for r in results if r['status'] == 'risco-alto')}")
    print(f"Itens subutilizados: {sum(1 for r in results if r['status'] == 'subutilizado')}")
    print(f"Vigência: {vigencia_meses} meses")
    print(f"Início: {inicio_contrato or 'não informado'}")
    print(f"Término: {termino_contrato or 'não informado'}")
    
    if inicio_contrato:
        try:
            inicio_dt = datetime.strptime(inicio_contrato, '%d/%m/%Y')
            termino_str = params.get('Término', '')
            if termino_str:
                termino_dt = datetime.strptime(termino_str, '%d/%m/%Y')
                delta = termino_dt - inicio_dt
                vigencia_meses = max(1, delta.days // 30)
            else:
                vigencia_str = params.get('Vigência', '24')
                try:
                    vigencia_meses = int(vigencia_str.replace('meses', '').strip())
                except:
                    pass
        except:
            vigencia_str = params.get('Vigência', '24')
            try:
                vigencia_meses = int(vigencia_str.replace('meses', '').strip())
            except:
                pass
    else:
        vigencia_str = params.get('Vigência', '24')
        try:
            vigencia_meses = int(vigencia_str.replace('meses', '').strip())
        except:
            pass
    
if __name__ == '__main__':
    main()