from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

doc = SimpleDocTemplate(
    "C:\\Users\\elson\\OneDrive\\Antigravity\\Grupo 3 - Gestão Contratual\\.agents\\skills\\analisador-memorial\\output\\7004259206_analise_memorial.pdf",
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
story.append(Paragraph("<b>Oportunidade:</b> 7004259206", normal_style))
story.append(Paragraph("<b>Documento:</b> Anexo 1 - Especificação dos Serviços (MD) - Rev. B", normal_style))
story.append(Paragraph("<b>Tipo:</b> Poço de Água Subterrânea - Sistema de Captação", normal_style))
story.append(Paragraph("<b>Área:</b> UN-SE/BA-1223 - Petrobrás", normal_style))
story.append(Spacer(1, 20))

story.append(Paragraph("1. RESUMO TÉCNICO DO OBJETO", heading_style))

story.append(Paragraph("<b>Objeto</b>", subheading_style))
story.append(Paragraph(
    "Construção de Poço de Água Subterrânea (Tubular Profundo) para captação de água potável no Estado da Bahia.",
    normal_style
))

story.append(Paragraph("<b>Características Principais</b>", subheading_style))
story.append(Paragraph("- Profundidade estimada: 120 metros", normal_style))
story.append(Paragraph("- Diâmetro de perfuração: 12 1/4\"", normal_style))
story.append(Paragraph("- Diâmetro do revestimento (casing): 6\" (SCH 40)", normal_style))
story.append(Paragraph("- Utilização: Abastecimento humano e industrial", normal_style))
story.append(Paragraph("- Localização: Estado da Bahia", normal_style))

story.append(Paragraph("<b>Método de Execução</b>", subheading_style))
story.append(Paragraph("- Perfuração rotativa com circulação de fluido (sistema lama)", normal_style))
story.append(Paragraph("- Sistema de completação com filtros (tela filter wire)", normal_style))
story.append(Paragraph("- Desenvolvimento do poço por meio de air-lift e/ou pistonagem", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("2. ESPECIFICAÇÕES TÉCNICAS E NORMAS APLICÁVEIS", heading_style))

story.append(Paragraph("<b>Normas ABNT</b>", subheading_style))
story.append(Paragraph("- NBR 12212: Poço profundo - Terminologia", normal_style))
story.append(Paragraph("- NBR 12214: Projeto de poço profundo para abastecimento de água", normal_style))
story.append(Paragraph("- NBR 12215: Poço profundo - Captação de água subterrânea", normal_style))
story.append(Paragraph("- NBR 12216: Poço profundo - Hidrogeologia", normal_style))
story.append(Paragraph("- NBR 13919: Poço profundo - Escopo de fornecimento do poço", normal_style))
story.append(Paragraph("- NBR 15527: Poço profundo - Determinação da vazão específica", normal_style))

story.append(Paragraph("<b>Normas Petrobrás</b>", subheading_style))
story.append(Paragraph("- N-2016: Especificação de materiais e equipamentos", normal_style))
story.append(Paragraph("- N-2022: Soldagem e inspeção de soldagem", normal_style))
story.append(Paragraph("- N-2036: Pintura - Esquema de pintura em atmosferas marítimas", normal_style))
story.append(Paragraph("- N-2090: Revestimento de poços tubulares profundos", normal_style))
story.append(Paragraph("- N-2157: Filtro de cascalho (gravel pack) para poços de água", normal_style))
story.append(Paragraph("- PET-2003D1: Teste de acceptance de fluido de perfuração", normal_style))

story.append(Paragraph("<b>Especificações de Materiais</b>", subheading_style))
story.append(Paragraph("<b>Revestimento (Casing):</b> Aço-carbono ASTM A53 Grau B ou API 5L Grau B, 6\", SCH 40, conexões rosca API BTC (buttress thread coupling)", normal_style))
story.append(Paragraph("<b>Revestimento interno:</b> Primer epóxi e revestimento epóxi fundido", normal_style))
story.append(Paragraph("<b>Filtros (Screens):</b> Tela armada (filter wire), furo de 1,0mm, material Aço inoxidável AISI 304 ou 316L", normal_style))
story.append(Paragraph("<b>Elementos Filtrantes:</b> Seixo rolado de silício (100% sílica) - granulometria conforme ensaio do aquífero", normal_style))

story.append(Paragraph("<b>Fluidos de Perfuração</b>", subheading_style))
story.append(Paragraph("Sistema de lama bentonítica com parâmetros de densidade, viscosidade, pH e teor de areias. Descarte conforme resolução CONAMA 420/2009.", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("3. RESPONSABILIDADES DA CONTRATADA", heading_style))

story.append(Paragraph("<b>A) Obrigações Operacionais</b>", subheading_style))
story.append(Paragraph("- Fornecimento de todo material de consumo (fluidos, etc)", normal_style))
story.append(Paragraph("- Execução da perfuração conforme diâmetro especificado", normal_style))
story.append(Paragraph("- Instalação do revestimento (casing) e filtros (screens)", normal_style))
story.append(Paragraph("- Fornecimento e instalação do elemento filtrante (seixo filtrante)", normal_style))
story.append(Paragraph("- Desenvolvimento do poço (air-lift/pistonagem) até estabilização", normal_style))
story.append(Paragraph("- Teste de vazão (vazão específica) antes da entrega", normal_style))

story.append(Paragraph("<b>B) Documentação e Registros</b>", subheading_style))
story.append(Paragraph("- Registro da estratigrafia (perfil litológico) durante perfuração", normal_style))
story.append(Paragraph("- Coleta de amostras de solo/rocha a cada metro perfurado", normal_style))
story.append(Paragraph("- Registro de perdas e ganhos de fluido", normal_style))
story.append(Paragraph("- Relatório final com perfil do poço completo", normal_style))

story.append(Paragraph("<b>C) Infraestrutura de Proteção</b>", subheading_style))
story.append(Paragraph("- Construção de caixa de proteção em concreto aparente", normal_style))
story.append(Paragraph("- Instalação de tampa de aço galvanizado", normal_style))
story.append(Paragraph("- Instalação de PVC ventilação conforme projeto", normal_style))

story.append(Paragraph("<b>D) Ensaios e Testes</b>", subheading_style))
story.append(Paragraph("- Ensaio de vazão específica (teste de aquífero)", normal_style))
story.append(Paragraph("- Análise físico-química da água (parâmetros de potabilidade)", normal_style))
story.append(Paragraph("- Ensaio de granulometria para definição do filtro", normal_style))
story.append(Paragraph("- Teste de acceptance do fluido de perfuração (PET-2003D1)", normal_style))

story.append(Paragraph("<b>E) Mobilização e Desmobilização</b>", subheading_style))
story.append(Paragraph("- Mobilização de equipamento de perfuração completo", normal_style))
story.append(Paragraph("- Desmobilização após conclusão e aceite", normal_style))

story.append(Paragraph("<b>F) Descarte e Limpeza</b>", subheading_style))
story.append(Paragraph("- Gerenciamento de resíduos conforme CONAMA 420/2009", normal_style))
story.append(Paragraph("- Destinação adequada de cascalho e fluido gasto", normal_style))
story.append(Paragraph("- Limpeza da área após conclusão dos serviços", normal_style))

story.append(Paragraph("<b>G) Responsável Técnico</b>", subheading_style))
story.append(Paragraph("Engenheiro de Poços ou Geólogo/Geohidrólogo com ART/CREA", normal_style))

story.append(Paragraph("<b>Documentação Exigida</b>", subheading_style))
story.append(Paragraph("- ART (Anotação de Responsabilidade Técnica) CREA", normal_style))
story.append(Paragraph("- Registro de perfuração (log de sonda)", normal_style))
story.append(Paragraph("- Relatório de ensaio de vazão", normal_style))
story.append(Paragraph("- Análise de potabilidade da água", normal_style))
story.append(Paragraph("- Certificados de materiais utilizados", normal_style))

story.append(Spacer(1, 15))
story.append(Paragraph("4. PRAZOS E MARCOS TÉCNICOS", heading_style))

story.append(Paragraph("<b>Etapas de Execução</b>", subheading_style))
story.append(Paragraph("1. <b>Mobilização</b> - Prazo a definir conforme cronograma contratual", normal_style))
story.append(Paragraph("2. <b>Perfuração</b> - Estima-se 15-20 dias úteis (variável conforme aquífero)", normal_style))
story.append(Paragraph("3. <b>Instalação de Revestimento e Filtros</b> - 2-3 dias após finalização da perfuração", normal_style))
story.append(Paragraph("4. <b>Desenvolvimento do Poço</b> - 5-10 dias (air-lift/pistonagem)", normal_style))
story.append(Paragraph("5. <b>Ensaio de Vazão Específica</b> - 2-3 dias após desenvolvimento", normal_style))
story.append(Paragraph("6. <b>Análise de Água</b> - 5-10 dias (laboratório externo)", normal_style))
story.append(Paragraph("7. <b>Desmobilização</b> - 1-2 dias após todos os ensaios", normal_style))

story.append(Paragraph("<b>Prazo Total Estimado:</b> 30-45 dias (sujeito às condições do aquífero)", normal_style))
story.append(Paragraph("Notas: Marcos técnicos sujeitos a ajustes conforme condições geológicas. Interrupções podem ocorrer em caso de problemas mecânicos ou condições climáticas.", normal_style))

story.append(Spacer(1, 30))
story.append(Paragraph("---", normal_style))
story.append(Paragraph("<b>Documento:</b> 02-Anexo 1-Especificação dos Serviços MD - Rev. B.pdf", normal_style))
story.append(Paragraph("<b>Oportunidade:</b> 7004259206", normal_style))
story.append(Paragraph("<b>Data:</b> 08/04/2026", normal_style))

doc.build(story)