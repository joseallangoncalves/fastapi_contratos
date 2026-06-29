from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Depends,
    HTTPException,
    status,
    Query,
    Path,
)
from typing import Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from services.llm_service import (
    process_document_with_skill,
    extract_text_from_pdf,
    extract_contract_metadata,
    estratificar_contrato,
    ingestao_metadados_contrato,
)
from database import get_db
from db_models import (
    AnaliseContratualDB,
    IngestaoMetadadosDB,
    ReconhecimentoEstratificacaoDB,
)
from utils import get_logger
from models import (
    AnaliseContratualResponse,
    AnaliseContratualUpdate,
    AnaliseContratualFullResponse,
    ReconhecimentoEstratificacaoResponse,
    ReconhecimentoEstratificacaoFullResponse,
    IngestaoMetadadosResponse,
)

logger = get_logger()
router = APIRouter()


# Helper para formatar retorno de estratificação
def format_estratificacao_db_to_response(
    db_entry: ReconhecimentoEstratificacaoDB,
) -> dict:
    return {
        "id": db_entry.id,
        "numero_contrato": db_entry.numero_contrato,
        "relatorio_assinatura": {
            "pagina_inicio": db_entry.relatorio_assinatura_inicio,
            "pagina_fim": db_entry.relatorio_assinatura_fim,
            "tipo": db_entry.relatorio_assinatura_tipo,
        },
        "instrumento_contratual_icj": {
            "pagina_inicio": db_entry.instrumento_contratual_icj_inicio,
            "pagina_fim": db_entry.instrumento_contratual_icj_fim,
            "tipo": db_entry.instrumento_contratual_icj_tipo,
        },
        "especificacao_tecnica_memorial": {
            "pagina_inicio": db_entry.especificacao_tecnica_memorial_inicio,
            "pagina_fim": db_entry.especificacao_tecnica_memorial_fim,
            "tipo": db_entry.especificacao_tecnica_memorial_tipo,
        },
        "planilha_precos_ppu": {
            "pagina_inicio": db_entry.planilha_precos_ppu_inicio,
            "pagina_fim": db_entry.planilha_precos_ppu_fim,
            "tipo": db_entry.planilha_precos_ppu_tipo,
        },
        "anexo_sms": {
            "pagina_inicio": db_entry.anexo_sms_inicio,
            "pagina_fim": db_entry.anexo_sms_fim,
            "tipo": db_entry.anexo_sms_tipo,
        },
        "circulares_conformidade": {
            "pagina_inicio": db_entry.circulares_conformidade_inicio,
            "pagina_fim": db_entry.circulares_conformidade_fim,
            "tipo": db_entry.circulares_conformidade_tipo,
        },
        "data_insercao": db_entry.data_insercao,
    }


# ==================================================================
# 1. ROTAS DE CRIAÇÃO / CADASTRO (POST)
# ==================================================================


# --- 1.1 RECONHECIMENTO E ESTRATIFICAÇÃO ---
@router.post(
    "/reconhecimento-estratificacao",
    response_model=ReconhecimentoEstratificacaoFullResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mapeamento e Estratificação de Documentos Contratuais",
    description="Recebe um contrato em PDF (tamanho máximo de 50MB), analisa o sumário e as primeiras páginas para mapear os intervalos de páginas de cada seção do contrato, além de extrair o número do contrato e salvar a análise no banco de dados.",
    response_description="Intervalos de páginas mapeados, número do contrato extraído e persistido com sucesso.",
    tags=["Análise de Contratos (IA)"],
)
async def reconhecimento_estratificacao(
    file: UploadFile = File(
        ...,
        description="Arquivo PDF do contrato ou documento a ser processado (formato aceito: .pdf, tamanho máximo: 50MB).",
    ),
    db: Session = Depends(get_db),
):
    """
    Recebe um contrato em PDF, analisa o sumário e as primeiras páginas para
    mapear os intervalos de páginas de cada seção do contrato, extrai o número do contrato e salva no banco.
    """
    logger.info("Endpoint /reconhecimento-estratificacao chamado.")
    print("\n--> [LOG] Endpoint /reconhecimento-estratificacao chamado.")
    resultado = await estratificar_contrato(file)

    # Limpar prefixo ICJ
    num_contrato = resultado.get("numero_contrato")
    if num_contrato:
        num_contrato_clean = num_contrato.strip()
        if num_contrato_clean.upper().startswith("ICJ"):
            num_contrato_clean = num_contrato_clean[3:].strip()
        resultado["numero_contrato"] = num_contrato_clean

    # Persistir no banco de dados
    db_entry = ReconhecimentoEstratificacaoDB(
        numero_contrato=resultado.get("numero_contrato"),
        relatorio_assinatura_inicio=resultado.get("relatorio_assinatura", {}).get(
            "pagina_inicio"
        )
        if resultado.get("relatorio_assinatura")
        else None,
        relatorio_assinatura_fim=resultado.get("relatorio_assinatura", {}).get(
            "pagina_fim"
        )
        if resultado.get("relatorio_assinatura")
        else None,
        relatorio_assinatura_tipo=resultado.get("relatorio_assinatura", {}).get("tipo")
        if resultado.get("relatorio_assinatura")
        else None,
        instrumento_contratual_icj_inicio=resultado.get(
            "instrumento_contratual_icj", {}
        ).get("pagina_inicio")
        if resultado.get("instrumento_contratual_icj")
        else None,
        instrumento_contratual_icj_fim=resultado.get(
            "instrumento_contratual_icj", {}
        ).get("pagina_fim")
        if resultado.get("instrumento_contratual_icj")
        else None,
        instrumento_contratual_icj_tipo=resultado.get(
            "instrumento_contratual_icj", {}
        ).get("tipo")
        if resultado.get("instrumento_contratual_icj")
        else None,
        especificacao_tecnica_memorial_inicio=resultado.get(
            "especificacao_tecnica_memorial", {}
        ).get("pagina_inicio")
        if resultado.get("especificacao_tecnica_memorial")
        else None,
        especificacao_tecnica_memorial_fim=resultado.get(
            "especificacao_tecnica_memorial", {}
        ).get("pagina_fim")
        if resultado.get("especificacao_tecnica_memorial")
        else None,
        especificacao_tecnica_memorial_tipo=resultado.get(
            "especificacao_tecnica_memorial", {}
        ).get("tipo")
        if resultado.get("especificacao_tecnica_memorial")
        else None,
        planilha_precos_ppu_inicio=resultado.get("planilha_precos_ppu", {}).get(
            "pagina_inicio"
        )
        if resultado.get("planilha_precos_ppu")
        else None,
        planilha_precos_ppu_fim=resultado.get("planilha_precos_ppu", {}).get(
            "pagina_fim"
        )
        if resultado.get("planilha_precos_ppu")
        else None,
        planilha_precos_ppu_tipo=resultado.get("planilha_precos_ppu", {}).get("tipo")
        if resultado.get("planilha_precos_ppu")
        else None,
        anexo_sms_inicio=resultado.get("anexo_sms", {}).get("pagina_inicio")
        if resultado.get("anexo_sms")
        else None,
        anexo_sms_fim=resultado.get("anexo_sms", {}).get("pagina_fim")
        if resultado.get("anexo_sms")
        else None,
        anexo_sms_tipo=resultado.get("anexo_sms", {}).get("tipo")
        if resultado.get("anexo_sms")
        else None,
        circulares_conformidade_inicio=resultado.get("circulares_conformidade", {}).get(
            "pagina_inicio"
        )
        if resultado.get("circulares_conformidade")
        else None,
        circulares_conformidade_fim=resultado.get("circulares_conformidade", {}).get(
            "pagina_fim"
        )
        if resultado.get("circulares_conformidade")
        else None,
        circulares_conformidade_tipo=resultado.get("circulares_conformidade", {}).get(
            "tipo"
        )
        if resultado.get("circulares_conformidade")
        else None,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    print("--> [LOG] Mapeamento e estratificação de contrato concluído e persistido.\n")
    return format_estratificacao_db_to_response(db_entry)


# --- 1.2 INGESTÃO DE METADADOS ---
@router.post(
    "/ingestao-metadados",
    response_model=IngestaoMetadadosResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingestão e Extração de Metadados Contratuais",
    description="Recebe um contrato em PDF (tamanho máximo de 50MB), extrai os principais metadados cadastrais utilizando IA (contratante, contratada, objeto, prazos e valor total) e os persiste no banco de dados.",
    response_description="Metadados extraídos e persistidos com sucesso.",
    tags=["Análise de Contratos (IA)"],
)
async def ingestao_metadados(
    file: UploadFile = File(
        ...,
        description="Arquivo PDF do contrato ou documento a ser processado (formato aceito: .pdf, tamanho máximo: 50MB).",
    ),
    db: Session = Depends(get_db),
):
    """
    Recebe um contrato em PDF, extrai os principais metadados cadastrais utilizando IA
    (contratante, contratada, objeto, prazos e valor total) e os persiste no banco de dados.
    """
    logger.info("Endpoint /ingestao-metadados chamado.")
    print("\n--> [LOG] Endpoint /ingestao-metadados chamado.")

    # 1. Extrair os metadados do PDF com a skill
    metadata = await ingestao_metadados_contrato(file)

    # Limpar prefixo ICJ
    num_contrato = metadata.get("numero_contrato")
    if num_contrato:
        num_contrato_clean = num_contrato.strip()
        if num_contrato_clean.upper().startswith("ICJ"):
            num_contrato_clean = num_contrato_clean[3:].strip()
        metadata["numero_contrato"] = num_contrato_clean

    # 2. Persistir no banco de dados
    db_entry = IngestaoMetadadosDB(
        numero_contrato=metadata.get("numero_contrato"),
        numero_oportunidade=metadata.get("numero_oportunidade"),
        objeto_contrato=metadata.get("objeto_contrato"),
        contratante=metadata.get("contratante"),
        contratada=metadata.get("contratada"),
        prazo_vigencia=metadata.get("prazo_vigencia"),
        prazo_execucao=metadata.get("prazo_execucao"),
        valor_total=metadata.get("valor_total"),
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    logger.info(f"Metadados persistidos com sucesso. ID: {db_entry.id}")
    print(f"--> [LOG] Metadados persistidos com sucesso no banco. ID: {db_entry.id}\n")

    return db_entry


# --- 1.3 ANÁLISE CONTRATUAL ---
@router.post(
    "/analise-contratual",
    response_model=AnaliseContratualResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Análise de Multas e Penalidades Contratuais",
    description="Recebe um contrato em PDF (tamanho máximo de 50MB), extrai cláusulas específicas de penalidades, multas, sanções e prazos de vigência utilizando IA e salva os dados de forma estruturada no banco de dados.",
    response_description="Análise realizada e salva no banco de dados com sucesso.",
    tags=["Análise de Contratos (IA)"],
)
async def analise_contratual(
    file: UploadFile = File(
        ...,
        description="Arquivo PDF do contrato ou documento a ser processado (formato aceito: .pdf, tamanho máximo: 50MB).",
    ),
    db: Session = Depends(get_db),
):
    """
    Recebe um contrato em PDF, extrai cláusulas específicas de penalidades,
    multas, sanções e prazos de vigência utilizando IA e salva os dados de forma estruturada no banco de dados.
    """
    logger.info("Endpoint /analise-contratual chamado.")
    print("\n--> [LOG] Endpoint /analise-contratual chamado.")

    # 1. Gerar o relatório de análise textual (markdown)
    resultado = await process_document_with_skill(file, "analisador-contratual")

    # 2. Resetar o ponteiro do arquivo para extrair o texto novamente para metadados
    await file.seek(0)
    file_bytes = await file.read()
    document_text = extract_text_from_pdf(file_bytes)

    # 3. Extrair metadados estruturados usando Gemini Structured Outputs
    metadata = await extract_contract_metadata(document_text)

    # Limpar prefixo ICJ
    num_contrato = metadata.get("numero_contrato")
    if num_contrato:
        num_contrato_clean = num_contrato.strip()
        if num_contrato_clean.upper().startswith("ICJ"):
            num_contrato_clean = num_contrato_clean[3:].strip()
        metadata["numero_contrato"] = num_contrato_clean

    # 4. Persistir no banco de dados
    db_entry = AnaliseContratualDB(
        empresa=metadata.get("empresa"),
        cnpj=metadata.get("cnpj"),
        data_inicio=metadata.get("data_inicio"),
        data_fim=metadata.get("data_fim"),
        vigencia_prazo=metadata.get("vigencia_prazo"),
        valor_contrato=metadata.get("valor_contrato"),
        clausula_vigencia=metadata.get("clausula_vigencia"),
        multas_moratorias=metadata.get("multas_moratorias"),
        multas_compensatorias=metadata.get("multas_compensatorias"),
        sancoes_administrativas=metadata.get("sancoes_administrativas"),
        rescisao=metadata.get("rescisao"),
        numero_contrato=metadata.get("numero_contrato"),
        numero_oportunidade=metadata.get("numero_oportunidade"),
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    logger.info(f"Análise persistida com sucesso no banco de dados. ID: {db_entry.id}")
    print(f"--> [LOG] Análise persistida com sucesso no banco. ID: {db_entry.id}\n")

    return {
        "id_analise": db_entry.id,
        "analise": {
            "clausula_vigencia": db_entry.clausula_vigencia,
            "multas_moratorias": db_entry.multas_moratorias,
            "multas_compensatorias": db_entry.multas_compensatorias,
            "sancoes_administrativas": db_entry.sancoes_administrativas,
            "rescisao": db_entry.rescisao,
        },
        "dados_salvos": {
            "empresa": db_entry.empresa,
            "cnpj": db_entry.cnpj,
            "data_inicio": db_entry.data_inicio,
            "data_fim": db_entry.data_fim,
            "vigencia_prazo": db_entry.vigencia_prazo,
            "valor_contrato": db_entry.valor_contrato,
            "data_insercao": db_entry.data_insercao.isoformat()
            if db_entry.data_insercao
            else None,
            "numero_contrato": db_entry.numero_contrato,
            "numero_oportunidade": db_entry.numero_oportunidade,
        },
    }


# ==================================================================
# 2. ROTAS DE CONSULTA / RECUPERAÇÃO (GET)
# ==================================================================


# --- 2.1 ESTRATIFICAÇÃO ---
@router.get(
    "/reconhecimento-estratificacao",
    response_model=List[ReconhecimentoEstratificacaoFullResponse],
    summary="Listar Estratificações de Páginas Persistidas",
    tags=["Consultas Gerais"],
)
async def listar_estratificacoes(
    numero_contrato: str | None = Query(
        None,
        description="Filtro por Número de Contrato. Requer exatamente 14 dígitos numéricos (com ou sem pontuação).",
        examples=["59000132964252"],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna uma lista de todas as estratificações de páginas de contratos salvas no banco de dados.
    Permite filtragem opcional por número do contrato.
    """
    logger.info("Endpoint GET /reconhecimento-estratificacao chamado.")
    query = db.query(ReconhecimentoEstratificacaoDB)
    if numero_contrato:
        # Validar quantidade de dígitos
        digits_only = "".join([c for c in numero_contrato if c.isdigit()])
        if len(digits_only) != 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número de contrato inválido ({numero_contrato}). O número de contrato deve conter exatamente 14 dígitos numéricos (ex: 5900.0132964.25.2).",
            )

        cleaned_input = (
            numero_contrato.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(" ", "")
            .upper()
        )
        if cleaned_input.startswith("ICJ"):
            cleaned_input = cleaned_input[3:]

        db_cleaned = func.replace(
            func.replace(
                func.replace(
                    func.replace(
                        ReconhecimentoEstratificacaoDB.numero_contrato, ".", ""
                    ),
                    "-",
                    "",
                ),
                " ",
                "",
            ),
            "ICJ",
            "",
        )
        query = query.filter(db_cleaned.ilike(f"%{cleaned_input}%"))

    results = query.order_by(ReconhecimentoEstratificacaoDB.data_insercao.desc()).all()
    return [format_estratificacao_db_to_response(res) for res in results]


@router.get(
    "/reconhecimento-estratificacao/{id}",
    response_model=ReconhecimentoEstratificacaoFullResponse,
    summary="Obter Detalhes de uma Estratificação Específica",
    tags=["Consultas Específicas"],
)
async def obter_estratificacao(
    id: int = Path(
        ...,
        description="ID numérico único da estratificação de páginas salva no banco de dados.",
        examples=[1],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna os detalhes completos de uma estratificação de páginas por ID.
    """
    logger.info(f"Endpoint GET /reconhecimento-estratificacao/{id} chamado.")
    db_entry = (
        db.query(ReconhecimentoEstratificacaoDB)
        .filter(ReconhecimentoEstratificacaoDB.id == id)
        .first()
    )
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Estratificação de contrato não encontrada."
        )
    return format_estratificacao_db_to_response(db_entry)


# --- 2.2 INGESTÃO DE METADADOS ---
@router.get(
    "/ingestao-metadados",
    response_model=List[IngestaoMetadadosResponse],
    summary="Listar Metadados Cadastrais Persistidos",
    tags=["Consultas Gerais"],
)
async def listar_metadados(
    numero_contrato: str | None = Query(
        None,
        description="Filtro por Número de Contrato. Requer exatamente 14 dígitos numéricos (com ou sem pontuação).",
        examples=["59000132964252"],
    ),
    contratada: str | None = Query(
        None,
        description="Filtro parcial por Razão Social da Empresa Contratada.",
        examples=["Petro"],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna uma lista de todos os registros de metadados de contratos persistidos.
    Permite filtragem opcional por número do contrato ou contratada.
    """
    logger.info("Endpoint GET /ingestao-metadados chamado.")
    query = db.query(IngestaoMetadadosDB)
    if numero_contrato:
        # Validar quantidade de dígitos
        digits_only = "".join([c for c in numero_contrato if c.isdigit()])
        if len(digits_only) != 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número de contrato inválido ({numero_contrato}). O número de contrato deve conter exatamente 14 dígitos numéricos (ex: 5900.0132964.25.2).",
            )

        cleaned_input = (
            numero_contrato.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(" ", "")
            .upper()
        )
        if cleaned_input.startswith("ICJ"):
            cleaned_input = cleaned_input[3:]

        db_cleaned = func.replace(
            func.replace(
                func.replace(
                    func.replace(IngestaoMetadadosDB.numero_contrato, ".", ""), "-", ""
                ),
                " ",
                "",
            ),
            "ICJ",
            "",
        )
        query = query.filter(db_cleaned.ilike(f"%{cleaned_input}%"))
    if contratada:
        query = query.filter(IngestaoMetadadosDB.contratada.ilike(f"%{contratada}%"))

    results = query.order_by(IngestaoMetadadosDB.data_insercao.desc()).all()
    return results


@router.get(
    "/ingestao-metadados/{id}",
    response_model=IngestaoMetadadosResponse,
    summary="Obter Detalhes de um Registro de Metadados Específico",
    tags=["Consultas Específicas"],
)
async def obter_metadados(
    id: int = Path(
        ...,
        description="ID numérico único do registro de metadados salvo no banco de dados.",
        examples=[1],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna os detalhes completos de um registro de metadados cadastrais específicos por ID.
    """
    logger.info(f"Endpoint GET /ingestao-metadados/{id} chamado.")
    db_entry = (
        db.query(IngestaoMetadadosDB).filter(IngestaoMetadadosDB.id == id).first()
    )
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Registro de metadados não encontrado."
        )
    return db_entry


# --- 2.3 ANÁLISE CONTRATUAL ---
@router.get(
    "/analises",
    summary="Listar Análises Contratuais Persistidas",
    tags=["Consultas Gerais"],
)
async def listar_analises(
    empresa: str | None = Query(
        None,
        description="Filtro parcial por Nome ou Razão Social da Empresa Contratada.",
        examples=["Petróleo"],
    ),
    cnpj: str | None = Query(
        None,
        description="Filtro por CNPJ da Contratada. Requer exatamente 14 dígitos numéricos (com ou sem pontuação).",
        examples=["12345678000199"],
    ),
    numero_contrato: str | None = Query(
        None,
        description="Filtro por Número de Contrato. Requer exatamente 14 dígitos numéricos (com ou sem pontuação).",
        examples=["59000132964252"],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna uma lista de todas as análises de contratos salvas no banco de dados.
    Permite filtragem opcional por empresa, CNPJ ou número do contrato.
    """
    logger.info("Endpoint GET /analises chamado.")
    query = db.query(AnaliseContratualDB)
    if empresa:
        query = query.filter(AnaliseContratualDB.empresa.ilike(f"%{empresa}%"))
    if cnpj:
        # Validar quantidade de dígitos
        digits_only_cnpj = "".join([c for c in cnpj if c.isdigit()])
        if len(digits_only_cnpj) != 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CNPJ inválido ({cnpj}). O CNPJ deve conter exatamente 14 dígitos numéricos (ex: 12.345.678/0001-99).",
            )

        cleaned_cnpj = (
            cnpj.replace(".", "").replace("-", "").replace("/", "").replace(" ", "")
        )
        db_cleaned_cnpj = func.replace(
            func.replace(func.replace(AnaliseContratualDB.cnpj, ".", ""), "-", ""),
            "/",
            "",
        )
        query = query.filter(db_cleaned_cnpj.ilike(f"%{cleaned_cnpj}%"))
    if numero_contrato:
        # Validar quantidade de dígitos
        digits_only = "".join([c for c in numero_contrato if c.isdigit()])
        if len(digits_only) != 14:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Número de contrato inválido ({numero_contrato}). O número de contrato deve conter exatamente 14 dígitos numéricos (ex: 5900.0132964.25.2).",
            )

        cleaned_input = (
            numero_contrato.replace(".", "")
            .replace("-", "")
            .replace("/", "")
            .replace(" ", "")
            .upper()
        )
        if cleaned_input.startswith("ICJ"):
            cleaned_input = cleaned_input[3:]

        db_cleaned = func.replace(
            func.replace(
                func.replace(
                    func.replace(AnaliseContratualDB.numero_contrato, ".", ""), "-", ""
                ),
                " ",
                "",
            ),
            "ICJ",
            "",
        )
        query = query.filter(db_cleaned.ilike(f"%{cleaned_input}%"))

    results = query.order_by(AnaliseContratualDB.data_insercao.desc()).all()
    return results


@router.get(
    "/analises/{id}",
    summary="Obter Detalhes de uma Análise Específica",
    tags=["Consultas Específicas"],
)
async def obter_analise(
    id: int = Path(
        ...,
        description="ID numérico único da análise contratual salva no banco de dados.",
        examples=[1],
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna os detalhes completos (incluindo todas as cláusulas salvas) de uma análise contratual específica por ID.
    """
    logger.info(f"Endpoint GET /analises/{id} chamado.")
    db_entry = (
        db.query(AnaliseContratualDB).filter(AnaliseContratualDB.id == id).first()
    )
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Análise contratual não encontrada."
        )
    return db_entry


# ==================================================================
# 3. OPERAÇÕES DE EDICAO / EXCLUSÃO (PATCH / DELETE)
# ==================================================================


@router.patch(
    "/analises/{id}",
    response_model=AnaliseContratualFullResponse,
    summary="Atualizar Parcialmente uma Análise Contratual",
    description="Atualiza apenas os campos enviados de uma análise contratual existente. Campos não enviados permanecem inalterados.",
    tags=["Alterações de dados"],
)
async def atualizar_analise(
    id: int = Path(
        ...,
        description="ID numérico único da análise contratual a ser editada.",
        examples=[1],
    ),
    dados: AnaliseContratualUpdate = None,
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente os dados de uma análise contratual.
    Apenas os campos enviados no body serão alterados; os demais permanecem como estão.
    """
    logger.info(f"Endpoint PATCH /analises/{id} chamado.")

    db_entry = (
        db.query(AnaliseContratualDB).filter(AnaliseContratualDB.id == id).first()
    )
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Análise contratual não encontrada."
        )

    update_data = dados.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Nenhum campo fornecido para atualização.",
        )

    for key, value in update_data.items():
        setattr(db_entry, key, value)

    db.commit()
    db.refresh(db_entry)

    logger.info(f"Análise contratual ID {id} atualizada com sucesso.")
    return db_entry


@router.delete(
    "/analises/{id}",
    summary="Excluir Análise Contratual",
    description="Exclui uma análise contratual do banco de dados. É necessário enviar o parâmetro `confirm=true` na query string para confirmar a exclusão.",
    tags=["Exclusão de registros"],
)
async def deletar_analise(
    id: int = Path(
        ...,
        description="ID numérico único da análise contratual a ser excluída.",
        examples=[1],
    ),
    confirm: bool = Query(
        False,
        description="Confirmação da exclusão (requer true para efetuar a ação).",
        examples=[True],
    ),
    db: Session = Depends(get_db),
):
    """
    Exclui uma análise contratual do banco de dados.
    A exclusão só é efetuada se o parâmetro `confirm=true` for enviado na query string.
    """
    logger.info(f"Endpoint DELETE /analises/{id} chamado.")

    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Exclusão não confirmada. Envie ?confirm=true para confirmar a exclusão.",
        )

    db_entry = (
        db.query(AnaliseContratualDB).filter(AnaliseContratualDB.id == id).first()
    )
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Análise contratual não encontrada."
        )

    db.delete(db_entry)
    db.commit()

    logger.info(f"Análise contratual ID {id} excluída com sucesso.")
    return {"mensagem": f"Análise contratual ID {id} excluída com sucesso."}
