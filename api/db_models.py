from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from datetime import datetime, timezone
from database import Base

class AnaliseContratualDB(Base):
    __tablename__ = "analises_contratuais"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    data_inicio = Column(Date, nullable=True)
    data_fim = Column(Date, nullable=True)
    vigencia_prazo = Column(Integer, nullable=True) # Prazo de vigência em meses (inteiro positivo)
    valor_contrato = Column(String, nullable=True)
    data_insercao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    clausula_vigencia = Column(Text, nullable=True) # Cópia textual da cláusula de vigência
    multas_moratorias = Column(Text, nullable=True)
    multas_compensatorias = Column(Text, nullable=True)
    sancoes_administrativas = Column(Text, nullable=True)
    rescisao = Column(Text, nullable=True)
    numero_contrato = Column(String, nullable=True)
    numero_oportunidade = Column(String, nullable=True)


class IngestaoMetadadosDB(Base):
    __tablename__ = "ingestao_metadados"

    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(String, nullable=True)
    numero_oportunidade = Column(String, nullable=True)
    objeto_contrato = Column(Text, nullable=True)
    contratante = Column(String, nullable=True)
    contratada = Column(String, nullable=True)
    prazo_vigencia = Column(Integer, nullable=True) # Prazo de vigência em meses
    prazo_execucao = Column(Integer, nullable=True) # Prazo de execução em meses
    valor_total = Column(String, nullable=True)
    data_insercao = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ReconhecimentoEstratificacaoDB(Base):
    __tablename__ = "reconhecimento_estratificacao"

    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(String, nullable=True)
    
    # Intervalos de páginas (Páginas inicial e final para cada seção)
    relatorio_assinatura_inicio = Column(Integer, nullable=True)
    relatorio_assinatura_fim = Column(Integer, nullable=True)
    relatorio_assinatura_tipo = Column(String, nullable=True)
    
    instrumento_contratual_icj_inicio = Column(Integer, nullable=True)
    instrumento_contratual_icj_fim = Column(Integer, nullable=True)
    instrumento_contratual_icj_tipo = Column(String, nullable=True)
    
    especificacao_tecnica_memorial_inicio = Column(Integer, nullable=True)
    especificacao_tecnica_memorial_fim = Column(Integer, nullable=True)
    especificacao_tecnica_memorial_tipo = Column(String, nullable=True)
    
    planilha_precos_ppu_inicio = Column(Integer, nullable=True)
    planilha_precos_ppu_fim = Column(Integer, nullable=True)
    planilha_precos_ppu_tipo = Column(String, nullable=True)
    
    anexo_sms_inicio = Column(Integer, nullable=True)
    anexo_sms_fim = Column(Integer, nullable=True)
    anexo_sms_tipo = Column(String, nullable=True)
    
    circulares_conformidade_inicio = Column(Integer, nullable=True)
    circulares_conformidade_fim = Column(Integer, nullable=True)
    circulares_conformidade_tipo = Column(String, nullable=True)
    
    data_insercao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
