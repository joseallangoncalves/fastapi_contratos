from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date


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
    data_inicio: date | None = Field(
        None, description="Data de início de vigência do contrato"
    )
    data_fim: date | None = Field(
        None, description="Data de fim de vigência do contrato"
    )
    vigencia_prazo: int | None = Field(
        None, description="Prazo de vigência do contrato em dias"
    )
    valor_contrato: str | None = Field(None, description="Valor global do contrato")
    data_insercao: str | None = Field(
        None, description="Data e hora em que o registro foi persistido no banco"
    )
    numero_contrato: str | None = Field(
        None, description="Número identificador do contrato extraído"
    )
    numero_oportunidade: str | None = Field(
        None, description="Número identificador da oportunidade extraído"
    )


class AnaliseDetalhada(BaseModel):
    clausula_vigencia: str | None = Field(
        None, description="Cláusula de vigência e prazo transcrita do contrato"
    )
    multas_moratorias: str | None = Field(
        None, description="Cláusulas de multas moratórias por atraso"
    )
    multas_compensatorias: str | None = Field(
        None, description="Cláusulas de multas compensatórias"
    )
    sancoes_administrativas: str | None = Field(
        None, description="Cláusulas de sanções administrativas"
    )
    rescisao: str | None = Field(None, description="Cláusulas de rescisão do contrato")


class AnaliseContratualResponse(BaseModel):
    id_analise: int = Field(
        ..., description="Identificador único da análise salva no banco de dados"
    )
    analise: AnaliseDetalhada = Field(
        ...,
        description="Objeto com as cláusulas detalhadas de multas e penalidades extraídas do contrato",
    )
    dados_salvos: AnaliseContratualDadosSalvos = Field(
        ..., description="Metadados estruturados extraídos e salvos"
    )


class AnaliseContratualUpdate(BaseModel):
    empresa: str | None = Field(
        None,
        description="Nome ou Razão Social da Empresa Contratada",
        example="EMPRESA CONSTRUTORA LTDA",
    )
    cnpj: str | None = Field(
        None, description="CNPJ da empresa contratada", example="12.345.678/0001-99"
    )
    data_inicio: date | None = Field(
        None, description="Data de início de vigência do contrato", example="2026-06-01"
    )
    data_fim: date | None = Field(
        None,
        description="Data de término de vigência do contrato",
        example="2027-06-01",
    )
    vigencia_prazo: int | None = Field(
        None, description="Prazo total de vigência do contrato em dias", example=365
    )
    valor_contrato: str | None = Field(
        None, description="Valor global do contrato", example="R$ 1.500.000,00"
    )
    clausula_vigencia: str | None = Field(
        None,
        description="Texto literal extraído sobre vigência",
        example="Cláusula 10ª - O prazo é de 12 meses...",
    )
    multas_moratorias: str | None = Field(
        None,
        description="Texto sobre multas de mora",
        example="Multa de 0,1% por dia de atraso...",
    )
    multas_compensatorias: str | None = Field(
        None,
        description="Texto sobre multas compensatórias",
        example="Multa compensatória de 10% sobre o saldo...",
    )
    sancoes_administrativas: str | None = Field(
        None,
        description="Texto sobre sanções aplicáveis",
        example="Advertência, suspensão temporária...",
    )
    rescisao: str | None = Field(
        None,
        description="Texto sobre condições de rescisão",
        example="Cláusula de rescisão com 30 dias de aviso prévio...",
    )
    numero_contrato: str | None = Field(
        None,
        description="Número único de identificação do contrato",
        example="5900.0132964.25.2",
    )
    numero_oportunidade: str | None = Field(
        None,
        description="Número da oportunidade Petronect associada",
        example="7004517339",
    )


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
    id: int = Field(
        ...,
        description="ID numérico único do registro de análise no banco de dados",
        example=1,
    )
    empresa: str | None = Field(
        None,
        description="Nome ou Razão Social da empresa contratada",
        example="EMPRESA CONSTRUTORA LTDA",
    )
    cnpj: str | None = Field(
        None, description="CNPJ da empresa contratada", example="12.345.678/0001-99"
    )
    data_inicio: date | None = Field(
        None, description="Data de início da vigência do contrato", example="2026-06-01"
    )
    data_fim: date | None = Field(
        None,
        description="Data de término da vigência do contrato",
        example="2027-06-01",
    )
    vigencia_prazo: int | None = Field(
        None, description="Prazo de vigência do contrato em dias", example=365
    )
    valor_contrato: str | None = Field(
        None, description="Valor global do contrato", example="R$ 1.500.000,00"
    )
    data_insercao: datetime | None = Field(
        None, description="Data e hora em que a análise foi salva no banco de dados"
    )
    clausula_vigencia: str | None = Field(
        None,
        description="Cópia textual das cláusulas de vigência e prazo",
        example="Cláusula 10ª - O prazo é de 12 meses...",
    )
    multas_moratorias: str | None = Field(
        None,
        description="Cópia textual das cláusulas de multas moratórias",
        example="Multa de 0,1% por dia de atraso...",
    )
    multas_compensatorias: str | None = Field(
        None,
        description="Cópia textual das cláusulas de multas compensatórias",
        example="Multa compensatória de 10%...",
    )
    sancoes_administrativas: str | None = Field(
        None, description="Cópia textual das cláusulas de sanções administrativas"
    )
    rescisao: str | None = Field(
        None, description="Cópia textual das cláusulas de rescisão"
    )
    numero_contrato: str | None = Field(
        None,
        description="Número identificador do contrato",
        example="5900.0132964.25.2",
    )
    numero_oportunidade: str | None = Field(
        None,
        description="Número identificador da oportunidade Petronect",
        example="7004517339",
    )


class SecaoIntervalo(BaseModel):
    pagina_inicio: int | None = Field(
        None, description="Primeira página da seção (1-indexed)"
    )
    pagina_fim: int | None = Field(
        None, description="Última página da seção (1-indexed)"
    )
    tipo: str | None = Field(
        None,
        description="Tipo predominante de conteúdo da seção ('Texto', 'Imagens', ou 'Texto + Imagens')",
    )


class ReconhecimentoEstratificacaoResponse(BaseModel):
    numero_contrato: str | None = Field(
        None, description="Número identificador do contrato"
    )
    relatorio_assinatura: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Relatório de Assinaturas"
    )
    instrumento_contratual_icj: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas do Instrumento Contratual Jurídico - ICJ",
    )
    especificacao_tecnica_memorial: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas da Especificação Técnica ou Memorial Descritivo",
    )
    planilha_precos_ppu: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas da Planilha de Preços Unitários (PPU)"
    )
    anexo_sms: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Anexo de SMS"
    )
    circulares_conformidade: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas de Circulares e relatórios de conformidade",
    )


class ReconhecimentoEstratificacaoFullResponse(BaseModel):
    id: int = Field(..., description="ID da estratificação salva no banco de dados")
    numero_contrato: str | None = Field(
        None, description="Número identificador do contrato"
    )
    relatorio_assinatura: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Relatório de Assinaturas"
    )
    instrumento_contratual_icj: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas do Instrumento Contratual Jurídico - ICJ",
    )
    especificacao_tecnica_memorial: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas da Especificação Técnica ou Memorial Descritivo",
    )
    planilha_precos_ppu: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas da Planilha de Preços Unitários (PPU)"
    )
    anexo_sms: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Anexo de SMS"
    )
    circulares_conformidade: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas de Circulares e relatórios de conformidade",
    )
    data_insercao: datetime | None = Field(
        None, description="Data e hora em que a estratificação foi persistida"
    )


class ReconhecimentoEstratificacaoUpdate(BaseModel):
    numero_contrato: str | None = Field(
        None, description="Número identificador do contrato"
    )
    relatorio_assinatura: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Relatório de Assinaturas"
    )
    instrumento_contratual_icj: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas do Instrumento Contratual Jurídico - ICJ",
    )
    especificacao_tecnica_memorial: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas da Especificação Técnica ou Memorial Descritivo",
    )
    planilha_precos_ppu: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas da Planilha de Preços Unitários (PPU)"
    )
    anexo_sms: SecaoIntervalo | None = Field(
        None, description="Intervalo de páginas do Anexo de SMS"
    )
    circulares_conformidade: SecaoIntervalo | None = Field(
        None,
        description="Intervalo de páginas de Circulares e relatórios de conformidade",
    )


class IngestaoMetadadosSchema(BaseModel):
    numero_contrato: str | None = Field(None, description="Número do contrato extraído")
    numero_oportunidade: str | None = Field(
        None, description="Número da oportunidade/identificação Petronect extraído"
    )
    objeto_contrato: str | None = Field(
        None, description="Objeto do contrato (resumo do escopo/serviços)"
    )
    contratante: str | None = Field(
        None, description="Razão social ou nome da entidade contratante"
    )
    contratada: str | None = Field(
        None, description="Razão social ou nome da empresa contratada"
    )
    prazo_vigencia: int | None = Field(
        None,
        description="Prazo de vigência do contrato em dias (número inteiro positivo)",
    )
    prazo_execucao: int | None = Field(
        None,
        description="Prazo de execução do contrato em dias (número inteiro positivo)",
    )
    valor_total: str | None = Field(
        None, description="Valor total/global do contrato (formato monetário)"
    )

    @field_validator("prazo_vigencia", "prazo_execucao")
    @classmethod
    def validate_positive_days(cls, v):
        if v is not None and v <= 0:
            raise ValueError(
                "O prazo em dias deve ser um número inteiro positivo maior que zero."
            )
        return v


class IngestaoMetadadosResponse(BaseModel):
    id: int = Field(
        ...,
        description="ID numérico único do registro cadastral no banco de dados",
        example=1,
    )
    numero_contrato: str | None = Field(
        None,
        description="Número identificador do contrato",
        example="5900.0132964.25.2",
    )
    numero_oportunidade: str | None = Field(
        None,
        description="Número identificador da oportunidade Petronect",
        example="7004517339",
    )
    objeto_contrato: str | None = Field(
        None,
        description="Objeto ou resumo dos serviços contratados",
        example="Serviços de manutenção preventiva e corretiva...",
    )
    contratante: str | None = Field(
        None,
        description="Razão Social ou Nome do Contratante",
        example="PETRÓLEO BRASILEIRO S.A. - PETROBRAS",
    )
    contratada: str | None = Field(
        None,
        description="Razão Social ou Nome da Empresa Contratada",
        example="EMPRESA CONSTRUTORA LTDA",
    )
    prazo_vigencia: int | None = Field(
        None, description="Prazo total de vigência do contrato em dias", example=365
    )
    prazo_execucao: int | None = Field(
        None, description="Prazo total de execução do contrato em dias", example=365
    )
    valor_total: str | None = Field(
        None, description="Valor global do contrato", example="R$ 1.500.000,00"
    )
    data_insercao: datetime | None = Field(
        None,
        description="Data e hora em que os metadados foram salvos no banco de dados",
    )


class IngestaoMetadadosUpdate(BaseModel):
    numero_contrato: str | None = Field(
        None, description="Número identificador do contrato"
    )
    numero_oportunidade: str | None = Field(
        None, description="Número da oportunidade Petronect"
    )
    objeto_contrato: str | None = Field(
        None, description="Objeto ou resumo dos serviços contratados"
    )
    contratante: str | None = Field(
        None, description="Razão Social ou Nome do Contratante"
    )
    contratada: str | None = Field(
        None, description="Razão Social ou Nome da Empresa Contratada"
    )
    prazo_vigencia: int | None = Field(
        None, description="Prazo total de vigência em dias", ge=1
    )
    prazo_execucao: int | None = Field(
        None, description="Prazo total de execução em dias", ge=1
    )
    valor_total: str | None = Field(None, description="Valor global do contrato")
