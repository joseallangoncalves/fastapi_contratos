# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Register font for Portuguese characters - use Windows built-in font
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))

output_path = "C:/Users/elson/OneDrive/Antigravity/Grupo 3 - Gestão Contratual/.agents/skills/analisador-sms/output/7004166210_SMS_analise.pdf"
doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
styles = getSampleStyleSheet()
story = []

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=18,
    textColor=HexColor('#1a365d'),
    spaceAfter=20,
    alignment=TA_CENTER
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=HexColor('#2c5282'),
    spaceBefore=20,
    spaceAfter=10
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=HexColor('#4a5568'),
    spaceBefore=15,
    spaceAfter=8
)

normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=6
)

# Title
story.append(Paragraph("RELATÓRIO DE ANÁLISE DE SMS", title_style))

# Header info
story.append(Paragraph("Código: SMS0048153 | Revisão: 05 | Contrato: 7004166210 (Lote 1)", normal_style))
story.append(Paragraph("Data: Fevereiro/2021", normal_style))
story.append(Spacer(1, 20))

# Summary
story.append(Paragraph("1. Resumo Executivo", h1_style))
story.append(Paragraph("Este documento estabelece os requisitos de Segurança, Saúde e Meio Ambiente (SMS) para execução de serviços integrados de manutenção industrial. O escopo abrange EPIs, treinamentos obrigatórios, procedimentos de emergência, gestão de resíduos, medicina ocupacional e obrigações tanto da Contratada quanto da Contratante.", normal_style))
story.append(Spacer(1, 15))

# EPIs
story.append(Paragraph("2. EPIs e Equipamentos de Proteção", h1_style))
epi_data = [
    ['EPI/Equipamento', 'Aplicação'],
    ['Capacete', 'Todas as áreas'],
    ['Óculos de proteção', 'Todas as áreas'],
    ['Calçado de segurança', 'Todas as áreas'],
    ['Protetor auricular', 'Áreas acima de 85 dB'],
    ['Luva de proteção', 'Conforme riscos específicos'],
    ['Creme protetor', 'Manuseio de produtos químicos'],
    ['Protetor facial', 'Soldagem e esmerilhamento'],
    ['Respirador', 'Atmosfera contaminada'],
    ['Cinto de segurança', 'Trabalho em altura'],
    ['Macacão', 'Áreas específicas']
]
epi_table = Table(epi_data, colWidths=[2.5*inch, 3.5*inch])
epi_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), Color(1, 1, 1)),
    ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOLD', (0, 0), (-1, 0), True),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, Color(0.7, 0.7, 0.7)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(epi_table)
story.append(Spacer(1, 10))

# Note
story.append(Paragraph("Observação: EPIs padrão da casa são fornecidos pela Contratante. A Contratada deve fornecer EPIs específicos para riscos especiais.", normal_style))
story.append(Spacer(1, 15))

# Treinamentos
story.append(Paragraph("3. Certificações e Treinamentos Obrigatórios", h1_style))
trein_data = [
    ['Treinamento', 'Aplicação', 'Periodicidade'],
    ['Integração (SST)', 'Todos os colaboradores', 'Início das atividades'],
    ['NR-10', 'Pessoal elétrico', 'Anual'],
    ['NR-35', 'Trabalho em altura', 'Anual'],
    ['NR-33', 'Espaço confinado', 'Anual'],
    ['NR-18', 'Construção civil', 'Atualização'],
    ['Combate a incêndio', 'Todos os colaboradores', 'Anual'],
    ['Primeiros socorros', 'Equipe designada', 'Anual'],
    ['Riscos químicos', 'Manipulação de produtos químicos', 'Anual'],
    ['Brigada de incêndio', 'Colaboradores designados', 'Anual']
]
trein_table = Table(trein_data, colWidths=[2*inch, 2*inch, 1.5*inch])
trein_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), Color(1, 1, 1)),
    ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOLD', (0, 0), (-1, 0), True),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, Color(0.7, 0.7, 0.7)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(trein_table)
story.append(Spacer(1, 15))

# Responsibilities
story.append(Paragraph("4. Tabela de Responsabilidades Cruzadas", h1_style))
resp_data = [
    ['Requisito', 'Contratada', 'Contratante'],
    ['EPI padrão', '', 'X'],
    ['EPI específico para riscos especiais', 'X', ''],
    ['Treinamentos obrigatórios', 'X', ''],
    ['Equipe de resposta a emergências', 'X', ''],
    ['Plano de Emergência da unidade', '', 'X'],
    ['Kit de primeiros socorros', 'X', ''],
    ['Atendimento pré-hospitalar', '', 'X'],
    ['Comunicação de incidentes', 'X', ''],
    ['Investigação de incidentes significativos', '', 'X'],
    ['Gestão de resíduos/rejeitos', 'X', ''],
    ['PPRA e PCMSO', 'X', ''],
    ['Exames admissionais/periódicos', 'X', ''],
    ['Fiscalização de SST', '', 'X'],
    ['Auditorias e inspeções', '', 'X']
]
resp_table = Table(resp_data, colWidths=[2.5*inch, 1*inch, 1*inch])
resp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), Color(1, 1, 1)),
    ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOLD', (0, 0), (-1, 0), True),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, Color(0.7, 0.7, 0.7)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(resp_table)
story.append(Spacer(1, 15))

# Points of attention
story.append(Paragraph("5. Pontos de Atenção", h1_style))
story.append(Paragraph("Pontos Críticos para a Contratada:", normal_style))
story.append(Paragraph("1. Não conformidades - Geram comunicação e registro no sistema de gestão", normal_style))
story.append(Paragraph("2. Exames médicos - Obrigatórios antes do início; não cumprimento pode gerar embargo", normal_style))
story.append(Paragraph("3. Treinamentos - Não cumprimento impede execução dos serviços", normal_style))
story.append(Paragraph("4. Incidentes - Todos devem ser comunicados imediatamente (inclusive quase-acidentes)", normal_style))
story.append(Paragraph("5. Documentação de SST - Deve estar atualizada e disponível para fiscalização", normal_style))
story.append(Spacer(1, 10))

story.append(Paragraph("Atenção Especial:", normal_style))
story.append(Paragraph("- NR-35 (Trabalho em altura) - Certificação anual obrigatória", normal_style))
story.append(Paragraph("- NR-33 (Espaço confinado) - Certificação obrigatória", normal_style))
story.append(Paragraph("- NR-10 (Atividades elétricas) - Certificação anual", normal_style))
story.append(Paragraph("- Áreas acima de 85 dB - Exige protetor auricular", normal_style))
story.append(Spacer(1, 15))

# Summary
story.append(Paragraph("6. Resumo de Quantitativos", h1_style))
summary_data = [
    ['EPIs', 'Treinamentos', 'Programas SST', 'NRs', 'Tipos de Exames'],
    ['10', '9', '5', '4', '4']
]
summary_table = Table(summary_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c5282')),
    ('TEXTCOLOR', (0, 0), (-1, 0), Color(1, 1, 1)),
    ('FONTNAME', (0, 0), (-1, 0), 'Arial'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOLD', (0, 0), (-1, 0), True),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ebf8ff')),
    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
    ('FONTSIZE', (0, 1), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 0.5, Color(0.7, 0.7, 0.7)),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
story.append(summary_table)
story.append(Spacer(1, 20))

# Footer
story.append(Paragraph("Documento gerado automaticamente via Skill analisador-sms | Data: 07/04/2026", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#718096'), alignment=TA_CENTER)))

doc.build(story)