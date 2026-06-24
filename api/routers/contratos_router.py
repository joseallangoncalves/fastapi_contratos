from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Query
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from services.llm_service import (
    process_document_with_skill,
    extract_text_from_pdf,
    extract_contract_metadata,
)
from database import get_db
from db_models import AnaliseContratualDB
from utils import get_logger
from models import (
    AnaliseContratualResponse,
    AnaliseContratualUpdate,
    AnaliseContratualFullResponse,
    AnaliseSMSResponse,
    GerarChecklistResponse,
)

logger = get_logger()
router = APIRouter()


@router.post(
    "/analise-contratual",
    response_model=AnaliseContratualResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Análise de Multas e Penalidades Contratuais",
    description="Recebe um contrato em PDF, extrai cláusulas específicas de penalidades, multas, sanções e prazos de vigência utilizando IA e salva os dados de forma estruturada no banco de dados.",
    response_description="Análise realizada e salva no banco de dados com sucesso.",
)
async def analise_contratual(
    file: UploadFile = File(...), db: Session = Depends(get_db)
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

    # 4. Persistir no banco de dados
    db_entry = AnaliseContratualDB(
        empresa=metadata.get("empresa"),
        cnpj=metadata.get("cnpj"),
        data_inicio=metadata.get("data_inicio"),
        data_fim=metadata.get("data_fim"),
        valor_contrato=metadata.get("valor_contrato"),
        vigencia_prazo=metadata.get("vigencia_prazo"),
        multas_moratorias=metadata.get("multas_moratorias"),
        multas_compensatorias=metadata.get("multas_compensatorias"),
        sancoes_administrativas=metadata.get("sancoes_administrativas"),
        rescisao=metadata.get("rescisao"),
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    logger.info(f"Análise persistida com sucesso no banco de dados. ID: {db_entry.id}")
    print(f"--> [LOG] Análise persistida com sucesso no banco. ID: {db_entry.id}\n")

    return {
        "id_analise": db_entry.id,
        "analise": resultado,
        "dados_salvos": {
            "empresa": db_entry.empresa,
            "cnpj": db_entry.cnpj,
            "data_inicio": db_entry.data_inicio,
            "data_fim": db_entry.data_fim,
            "valor_contrato": db_entry.valor_contrato,
            "data_insercao": db_entry.data_insercao.isoformat()
            if db_entry.data_insercao
            else None,
        },
    }


@router.post(
    "/analise-sms",
    response_model=AnaliseSMSResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Análise de Requisitos SMS",
    description="Recebe um anexo/contrato em PDF e extrai obrigações de Segurança, Meio Ambiente e Saúde aplicáveis à Contratada.",
    response_description="Obrigações de SMS extraídas com sucesso.",
)
async def analise_sms(file: UploadFile = File(...)):
    """
    Recebe um anexo/contrato em PDF e extrai obrigações de
    Segurança, Meio Ambiente e Saúde aplicáveis à Contratada.
    """
    logger.info("Endpoint /analise-sms chamado.")
    print("\n--> [LOG] Endpoint /analise-sms chamado.")
    resultado = await process_document_with_skill(file, "analisador-sms")
    print("--> [LOG] Análise de SMS concluída com sucesso.\n")
    return {"analise": resultado}


@router.post(
    "/gerar-checklist",
    response_model=GerarChecklistResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Geração de Checklist de Fiscalização",
    description="Recebe um contrato em PDF e gera automaticamente um checklist de verificação para apoiar o processo de recebimento e fiscalização.",
    response_description="Checklist gerado com sucesso.",
)
async def gerar_checklist(file: UploadFile = File(...)):
    """
    Recebe um contrato em PDF e gera automaticamente um checklist de verificação
    para apoiar o processo de recebimento e fiscalização.
    """
    logger.info("Endpoint /gerar-checklist chamado.")
    print("\n--> [LOG] Endpoint /gerar-checklist chamado.")
    resultado = await process_document_with_skill(file, "gerador-checklist-contratual")
    print("--> [LOG] Checklist gerado com sucesso.\n")
    return {"analise": resultado}


@router.get("/analises", summary="Listar Análises Contratuais Persistidas")
async def listar_analises(
    empresa: str | None = None, cnpj: str | None = None, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de todas as análises de contratos salvas no banco de dados.
    Permite filtragem opcional por empresa ou CNPJ.
    """
    logger.info("Endpoint GET /analises chamado.")
    query = db.query(AnaliseContratualDB)
    if empresa:
        query = query.filter(AnaliseContratualDB.empresa.ilike(f"%{empresa}%"))
    if cnpj:
        query = query.filter(AnaliseContratualDB.cnpj == cnpj)

    results = query.order_by(AnaliseContratualDB.data_insercao.desc()).all()
    return results


@router.get("/analises/{id}", summary="Obter Detalhes de uma Análise Específica")
async def obter_analise(id: int, db: Session = Depends(get_db)):
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


@router.patch(
    "/analises/{id}",
    response_model=AnaliseContratualFullResponse,
    summary="Atualizar Parcialmente uma Análise Contratual",
    description="Atualiza apenas os campos enviados de uma análise contratual existente. Campos não enviados permanecem inalterados.",
)
async def atualizar_analise(
    id: int, dados: AnaliseContratualUpdate, db: Session = Depends(get_db)
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
)
async def deletar_analise(
    id: int, confirm: bool = Query(False), db: Session = Depends(get_db)
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
