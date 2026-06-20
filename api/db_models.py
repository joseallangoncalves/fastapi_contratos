from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from database import Base

class AnaliseContratualDB(Base):
    __tablename__ = "analises_contratuais"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    data_inicio = Column(String, nullable=True)
    data_fim = Column(String, nullable=True)
    valor_contrato = Column(String, nullable=True)
    data_insercao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    vigencia_prazo = Column(Text, nullable=True)
    multas_moratorias = Column(Text, nullable=True)
    multas_compensatorias = Column(Text, nullable=True)
    sancoes_administrativas = Column(Text, nullable=True)
    rescisao = Column(Text, nullable=True)
