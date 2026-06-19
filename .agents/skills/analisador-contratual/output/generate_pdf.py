# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor

doc = SimpleDocTemplate(
    "C:\\Users\\elson\\OneDrive\\Antigravity\\Grupo 3 - Gestão Contratual\\.agents\\skills\\analisador-contratual\\output\\7004259206_analise_contratual.pdf",
    pagesize=letter,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=18,
    textColor=HexColor('#c0392b'),
    spaceAfter=20,
    alignment=1
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=HexColor('#333333'),
    spaceBefore=20,
    spaceAfter=10,
    borderPadding=5,
    borderWidth=1,
    borderColor=HexColor('#c0392b')
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=HexColor('#666666'),
    alignment=1,
    spaceAfter=30
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    textColor=HexColor('#333333'),
    spaceAfter=8
)

bold_style = ParagraphStyle(
    'CustomBold',
    parent=styles['Normal'],
    fontSize=10,
    textColor=HexColor('#333333'),
    spaceAfter=8
)

story.append(Paragraph("RELATÓRIO DE PENALIDADES E RISCOS CONTRATUAIS", title_style))
story.append(Paragraph("Análise de Minuta Contratual", subtitle_style))

story.append(Paragraph("DADOS DO CONTRATO", heading_style))
story.append(Paragraph("<b>Oportunidade:</b> 7004259206", normal_style))
story.append(Paragraph("<b>Contratada:</b> SOLUTI SOLUCOES CORPORATIVAS LTDA", normal_style))
story.append(Paragraph("<b>CNPJ:</b> 04.605.026/0001-54", normal_style))

story.append(Paragraph("VIGÊNCIA", heading_style))
story.append(Paragraph("<b>Início:</b> 02 de janeiro de 2025", normal_style))
story.append(Paragraph("<b>Término:</b> 01 de janeiro de 2027", normal_style))
story.append(Paragraph("<b>Duração:</b> 24 meses (2 anos)", normal_style))
story.append(Paragraph("<b>Valor Total:</b> R$ 717.600,00", normal_style))

story.append(Paragraph("MULTAS E PENALIDADES", heading_style))

data = [
    ['Tipo', 'Percentual', 'Condição'],
    ['Multa Moratória', '0,5% ao dia', 'Por dia de atraso (limitada a 10%)'],
    ['Multa Compensatória', '10%', 'Descumprimento total do objeto'],
    ['Multa por Não Execução', '10%', 'Sobre valor da ordem de serviço não executada']
]

table = Table(data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#c0392b')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
    ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#333333')),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 1, HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(table)

story.append(Paragraph("SANÇÕES ADMINISTRATIVAS (Art. 7º Lei 10.520/02)", heading_style))
sanctions = [
    "Advertência",
    "Multa",
    "Suspensão de participação em licitações por até 5 anos",
    "Declaração de idoneidade para licitar e contratar com a Administração Pública"
]
for s in sanctions:
    story.append(Paragraph(f"• {s}", normal_style))

story.append(Paragraph("CONDIÇÕES DE RESCISÃO", heading_style))
rescisao = [
    "Descumprimento de cláusulas contratuais, especificações técnicas e cronogramas",
    "Decretação de falência, recuperação judicial ou extrajudicial da Contratada",
    "Dissolução, fusão ou incorporação da Contratada",
    "Subcontratação não autorizada total ou parcial",
    "Cometimento de falhas reiteradas que comprometam a execução do objeto",
    "Não regularização de documento de regularidade fiscal no prazo de 5 dias",
    "Manifesto de insatisfação dos serviços pela Contratada"
]
for r in rescisao:
    story.append(Paragraph(f"• {r}", normal_style))

story.append(Paragraph("PENALIDADES APLICÁVEIS À CONTRATADA", heading_style))
penalidades = [
    "Multa moratória: 0,5% (meio por cento) por dia de atraso, limitada a 10% do valor do Item/Etapa/Marcos",
    "Multa compensatória: 10% (dez por cento) do valor total do contrato em caso de descumprimento total",
    "Multa de 10% sobre o valor da ordem de serviço em caso de não execução do serviço",
    "Suspensão temporária de participação em licitações (até 5 anos)",
    "Declaração de idoneidade para licitar e contratar com a Administração Pública",
    "Rescisão contratual por inadimplemento"
]
for p in penalidades:
    story.append(Paragraph(f"• {p}", normal_style))

story.append(Paragraph("CONDIÇÕES DE IMPACTO", heading_style))
story.append(Paragraph("<b>Base de Cálculo:</b> Valor do Item/Etapa/Marcos ou valor total do contrato", normal_style))
story.append(Paragraph("<b>Índice de Correção:</b> IPCA-E em caso de inadimplência", normal_style))

story.append(Paragraph("RISCO IDENTIFICADO", heading_style))
story.append(Paragraph("<b>Nível: ALTO</b>", normal_style))
story.append(Paragraph("Atrasos na entrega ou execução dos serviços podem gerar:", normal_style))
riscos = [
    "Multa diária de 0,5% limitada a 10% por etapa/item",
    "Multa compensatória de 10% do valor total do contrato",
    "Rescisão contratual por inadimplemento",
    "Sanções administrativas (suspensão/idoneidade)"
]
for r in riscos:
    story.append(Paragraph(f"• {r}", normal_style))

story.append(Spacer(1, 20))
story.append(Paragraph("══════════════════════════════════════════════════════════════", subtitle_style))
story.append(Paragraph("Relatório gerado em: 08/04/2026 | Skill: analisador-contratual", subtitle_style))

doc.build(story)