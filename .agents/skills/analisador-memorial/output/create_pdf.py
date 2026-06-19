from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

doc = SimpleDocTemplate(
    "C:\\Users\\elson\\OneDrive\\Antigravity\\Grupo 3 - Gestão Contratual\\.agents\\skills\\analisador-memorial\\output\\7004166210_analise_memorial.pdf",
    pagesize=letter,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72
)

styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    spaceAfter=20,
    textColor=colors.HexColor('#004a99')
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    spaceAfter=12,
    textColor=colors.HexColor('#004a99'),
    borderPadding=10,
    borderColor=colors.HexColor('#004a99'),
    borderWidth=2
)

subheading_style = ParagraphStyle(
    'CustomSubheading',
    parent=styles['Heading3'],
    fontSize=12,
    spaceAfter=8,
    textColor=colors.HexColor('#0066cc')
)

normal_style = styles['Normal']
normal_style.fontSize = 10
normal_style.spaceAfter = 8

story.append(Paragraph("Anexo I - Especificação Técnica", title_style))
story.append(Paragraph("<b>Oportunidade:</b> 7004166210", normal_style))
story.append(Paragraph("<b>Contrato:</b> Adequação de Infraestrutura de Rede e Segurança", normal_style))
story.append(Paragraph("<b>Contratante:</b> PETROBRAS", normal_style))
story.append(Paragraph("<b>Lotes:</b> 1 e 2", normal_style))
story.append(Spacer(1, 20))

story.append(Paragraph("1. MEMORIAL DESCRITIVO", heading_style))

story.append(Paragraph("<b>Resumo do Objeto</b>", subheading_style))
story.append(Paragraph(
    "Contratação de serviços de adequação de infraestrutura de rede e segurança em diversas unidades da PETROBRAS, contemplando duas linhas de escopo principais:",
    normal_style
))
story.append(Paragraph(
    "- <b>Lote 1:</b> Adequação de rede lógica, wi-fi, circuito de voz, infraestrutura física, ativos de rede e segurança",
    normal_style
))
story.append(Paragraph(
    "- <b>Lote 2:</b> Adequação de infraestrutura de energia, SPDA, climatização, iluminação, obras civis e cabeamento estruturado",
    normal_style
))

story.append(Paragraph("<b>Local</b>", subheading_style))
story.append(Paragraph(
    "Instalações da PETROBRAS em diversas localidades, incluindo refinarias (REGAP, RLAM, REPLAN, RPBC, REDUC), terminais (TEBAR, TESUT, TEPAC), centrais de processamento e unidades administrativas.",
    normal_style
))

story.append(Paragraph("<b>Objetivos Principais</b>", subheading_style))
story.append(Paragraph("- Modernização da infraestrutura de rede e segurança", normal_style))
story.append(Paragraph("- Implantação de sistemas de wi-fi corporativo e visitantes", normal_style))
story.append(Paragraph("- Atualização de ativos de rede", normal_style))
story.append(Paragraph("- Adequação de infraestrutura física e energética", normal_style))
story.append(Paragraph("- Conformidade com normas técnicas (ABNT, PETROBRAS, ISO)", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("2. ESPECIFICAÇÕES TÉCNICAS", heading_style))

story.append(Paragraph("<b>Normas Aplicáveis</b>", subheading_style))
story.append(Paragraph("<b>ABNT:</b> NBR 14565, NBR 5410, NBR 13535, NBR 5419, NBR 10152", normal_style))
story.append(Paragraph("<b>ISO/IEC:</b> ISO/IEC 11801, ISO 27001, ISO 27002, ISO 22301, ISO 9001, ISO 14001, ISO 45001", normal_style))
story.append(Paragraph("<b>ANSI/TIA:</b> TIA-568, TIA-569, TIA-606, TIA-607", normal_style))
story.append(Paragraph("<b>Normas PETROBRAS:</b> N-001 a N-1000 (diversas especificações)", normal_style))

story.append(Paragraph("<b>Materiais e Equipamentos</b>", subheading_style))
story.append(Paragraph("- Cabeamento U/UTP Cat 6A ou superior", normal_style))
story.append(Paragraph("- Switches gerenciáveis, routers, firewalls, access points Wi-Fi 6E", normal_style))
story.append(Paragraph("- Eletrocalhas, canaletas, racks, bastidores", normal_style))
story.append(Paragraph("- UPS, estabilizadores, disjuntores, cabos de energia", normal_style))
story.append(Paragraph("- Sistema de SPDA", normal_style))
story.append(Paragraph("- Equipamentos de climatização com redundância N+1", normal_style))
story.append(Paragraph("- Iluminação LED", normal_style))

story.append(Paragraph("<b>Métodos Executivos</b>", subheading_style))
story.append(Paragraph("- Instalação conforme TIA-568 e NBR 14565", normal_style))
story.append(Paragraph("- Certificação de rede (TIA-606, NBR IEC 60512)", normal_style))
story.append(Paragraph("- Testes de continuidade, Performance Test e Wire Map", normal_style))
story.append(Paragraph("- Configuração de VLANs, STP, RSTP, MSTP, EtherChannel", normal_style))
story.append(Paragraph("- Segurança Wi-Fi (WPA3, 802.1X)", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("3. RESPONSABILIDADES DA CONTRATADA", heading_style))

story.append(Paragraph("<b>Mobilização e Pessoal</b>", subheading_style))
story.append(Paragraph("- Disponibilizar equipe técnica qualificada", normal_style))
story.append(Paragraph("- Fornecer técnicos certificados para ativos de rede", normal_style))
story.append(Paragraph("- Disponibilizar Engenheiro RT registrado no CREA", normal_style))
story.append(Paragraph("- Custos de mobilização e desmobilização", normal_style))

story.append(Paragraph("<b>Fornecimento de Materiais</b>", subheading_style))
story.append(Paragraph("- Fornecer todos os materiais necessários", normal_style))
story.append(Paragraph("- Materiais novos e de primeira qualidade", normal_style))
story.append(Paragraph("- Ferramentas, instrumentos de medição e EPIs", normal_style))

story.append(Paragraph("<b>Infraestrutura e Instalações</b>", subheading_style))
story.append(Paragraph("- Instalação de cabeamento estruturado", normal_style))
story.append(Paragraph("- Instalação de eletrocalhas e canaletas", normal_style))
story.append(Paragraph("- Obras civis (prumadas, salas técnicas)", normal_style))
story.append(Paragraph("- Sistema de SPDA", normal_style))
story.append(Paragraph("- Sistema de climatização", normal_style))
story.append(Paragraph("- Infraestrutura de energia (UPS)", normal_style))

story.append(Paragraph("<b>Qualidade e Certificações</b>", subheading_style))
story.append(Paragraph("- Certificação do sistema de cabeamento", normal_style))
story.append(Paragraph("- Testes de Acceptance Test e Performance Test", normal_style))
story.append(Paragraph("- Laudos técnicos e relatórios", normal_style))
story.append(Paragraph("- Conformidade com normas técnicas", normal_style))
story.append(Paragraph("- Aprovação da fiscalização PETROBRAS", normal_style))

story.append(Paragraph("<b>Segurança e Meio Ambiente</b>", subheading_style))
story.append(Paragraph("- Medidas de segurança conforme NRs", normal_style))
story.append(Paragraph("- EPIs", normal_style))
story.append(Paragraph("- Normas de SMS PETROBRAS", normal_style))
story.append(Paragraph("- Gerenciamento de resíduos", normal_style))

story.append(Paragraph("<b>Documentação Técnica</b>", subheading_style))
story.append(Paragraph("- Projetos as-built", normal_style))
story.append(Paragraph("- Manual de operação e manutenção", normal_style))
story.append(Paragraph("- Diagramas lógicos e físicos da rede", normal_style))
story.append(Paragraph("- Configurações de ativos de rede", normal_style))
story.append(Paragraph("- Inventário de materiais", normal_style))

story.append(Paragraph("<b>Testes e Comissionamento</b>", subheading_style))
story.append(Paragraph("- Testes conforme especificações", normal_style))
story.append(Paragraph("- Comissionamento completo", normal_style))
story.append(Paragraph("- Testes de integração", normal_style))
story.append(Paragraph("- Testes de redundância e fail-over", normal_style))
story.append(Paragraph("- Testes de desempenho", normal_style))

story.append(Paragraph("<b>Garantia e Suporte</b>", subheading_style))
story.append(Paragraph("- Garantia mínima de 12 meses", normal_style))
story.append(Paragraph("- Suporte técnico durante garantia", normal_style))
story.append(Paragraph("- Substituição de materiais defeituosos", normal_style))
story.append(Paragraph("- Correções sem custo adicional", normal_style))

story.append(Paragraph("<b>Segurança da Informação</b>", subheading_style))
story.append(Paragraph("- Controles ISO 27001 e ISO 27002", normal_style))
story.append(Paragraph("- Políticas de segurança PETROBRAS", normal_style))
story.append(Paragraph("- Segmentação de rede", normal_style))
story.append(Paragraph("- Firewalls e IDS/IPS", normal_style))
story.append(Paragraph("- Backup e recuperação", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("4. PRAZOS E MARCOS TÉCNICOS", heading_style))

story.append(Paragraph("<b>Prazos</b>", subheading_style))
story.append(Paragraph("- Prazo Total: A definir conforme contrato", normal_style))
story.append(Paragraph("- Período de Garantia: Mínimo 12 meses após recebimento definitivo", normal_style))

story.append(Paragraph("<b>Marcos de Entrega</b>", subheading_style))
story.append(Paragraph("1. Entrega do Projeto - Aprovação do projeto executivo", normal_style))
story.append(Paragraph("2. Mobilização - Início de mobilização", normal_style))
story.append(Paragraph("3. Infraestrutura - Conclusão da infraestrutura física", normal_style))
story.append(Paragraph("4. Cabeamento - Instalação e certificação", normal_style))
story.append(Paragraph("5. Ativos - Instalação e configuração", normal_style))
story.append(Paragraph("6. Comissionamento - Testes e validações", normal_style))
story.append(Paragraph("7. Homologação - Testes de aceite", normal_style))
story.append(Paragraph("8. Recebimento Provisório", normal_style))
story.append(Paragraph("9. Recebimento Definitivo - Após 12 meses", normal_style))

story.append(Spacer(1, 30))
story.append(Paragraph("---", normal_style))
story.append(Paragraph("<b>Documento:</b> Anexo 01 - Especificação Técnica Rev.pdf", normal_style))
story.append(Paragraph("<b>Oportunidade:</b> 7004166210", normal_style))
story.append(Paragraph("<b>Data:</b> 07/04/2026", normal_style))

doc.build(story)
