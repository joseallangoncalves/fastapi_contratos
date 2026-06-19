from fastapi import APIRouter, File, UploadFile
from typing import Dict
from services.llm_service import process_document_with_skill
from utils import get_logger

logger = get_logger()
router = APIRouter()

@router.post("/analise-contratual", summary="Análise de Multas e Penalidades Contratuais")
async def analise_contratual(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Recebe um contrato em PDF e extrai cláusulas específicas de penalidades, 
    multas, sanções e prazos de vigência utilizando IA.
    """
    logger.info("Endpoint /analise-contratual chamado.")
    resultado = await process_document_with_skill(file, "analisador-contratual")
    return {"analise": resultado}

@router.post("/analise-sms", summary="Análise de Requisitos SMS")
async def analise_sms(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Recebe um anexo/contrato em PDF e extrai obrigações de 
    Segurança, Meio Ambiente e Saúde aplicáveis à Contratada.
    """
    logger.info("Endpoint /analise-sms chamado.")
    resultado = await process_document_with_skill(file, "analisador-sms")
    return {"analise": resultado}

@router.post("/gerar-checklist", summary="Geração de Checklist de Fiscalização")
async def gerar_checklist(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Recebe um contrato em PDF e gera automaticamente um checklist de verificação 
    para apoiar o processo de recebimento e fiscalização.
    """
    logger.info("Endpoint /gerar-checklist chamado.")
    resultado = await process_document_with_skill(file, "gerador-checklist-contratual")
    return {"analise": resultado}
