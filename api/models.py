from pydantic import BaseModel, Field
from datetime import datetime


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class AnaliseContratualDadosSalvos(BaseModel):
    empresa: str | None = Field(
        None, description="Nome da empresa contratada extraído do documento"
    )
    cnpj: str | None = Field(
        None, description="CNPJ da empresa contratada extraído do documento"
    )
    data_inicio: str | None = Field(
        None, description="Data de início de vigência do contrato"
    )
    data_fim: str | None = Field(
        None, description="Data de fim de vigência do contrato"
    )
    valor_contrato: str | None = Field(None, description="Valor global do contrato")
    data_insercao: str | None = Field(
        None, description="Data e hora em que o registro foi persistido no banco"
    )


class AnaliseContratualResponse(BaseModel):
    id_analise: int = Field(
        ..., description="Identificador único da análise salva no banco de dados"
    )
    analise: str = Field(
        ...,
        description="Relatório de análise de multas e penalidades gerado pela IA em Markdown",
    )
    dados_salvos: AnaliseContratualDadosSalvos = Field(
        ..., description="Metadados estruturados extraídos e salvos"
    )


class AnaliseContratualUpdate(BaseModel):
    empresa: str | None = None
    cnpj: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    valor_contrato: str | None = None
    vigencia_prazo: str | None = None
    multas_moratorias: str | None = None
    multas_compensatorias: str | None = None
    sancoes_administrativas: str | None = None
    rescisao: str | None = None


class AnaliseSMSResponse(BaseModel):
    analise: str = Field(
        ...,
        description="Relatório de obrigações de Saúde, Segurança e Meio Ambiente (SMS) gerado em Markdown",
    )


class GerarChecklistResponse(BaseModel):
    analise: str = Field(
        ...,
        description="Checklist estruturado para fiscalização e recebimento contratual em Markdown",
    )


class AnaliseContratualFullResponse(BaseModel):
    id: int
    empresa: str | None = None
    cnpj: str | None = None
    data_inicio: str | None = None
    data_fim: str | None = None
    valor_contrato: str | None = None
    data_insercao: datetime | None = None
    vigencia_prazo: str | None = None
    multas_moratorias: str | None = None
    multas_compensatorias: str | None = None
    sancoes_administrativas: str | None = None
    rescisao: str | None = None
