import os
from pathlib import Path
import fitz  # PyMuPDF
from fastapi import UploadFile, HTTPException
from utils import execute_prompt, execute_structured_prompt, get_logger

logger = get_logger()

# Diretório raiz onde a pasta .agents está localizada
BASE_DIR = Path(__file__).parent.parent.parent
SKILLS_DIR = BASE_DIR / ".agents" / "skills"


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrai texto de um arquivo PDF usando PyMuPDF (fitz) e valida se é digitalizável."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        logger.error(f"Erro ao abrir arquivo PDF: {e}")
        raise HTTPException(
            status_code=400,
            detail="Erro ao processar o arquivo PDF. Verifique se o arquivo está corrompido ou é inválido."
        )

    text = ""
    for page in doc:
        text += page.get_text() + "\n"

    extracted = text.strip()
    if not extracted:
        msg = "O arquivo PDF fornecido está digitalizado (imagem) ou não contém texto selecionável. Para realizar a análise, envie um PDF pesquisável (com texto digital selecionável)."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )
    return extracted


def get_skill_prompt(skill_name: str) -> str:
    """Lê o conteúdo do arquivo SKILL.md de uma skill específica."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        logger.error(f"Skill '{skill_name}' não encontrada em {skill_path}")
        raise HTTPException(status_code=500, detail=f"Skill '{skill_name}' não configurada no servidor.")
    
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Erro ao ler arquivo da skill {skill_name}: {e}")
import asyncio

async def process_document_with_skill(file: UploadFile, skill_name: str) -> str:
    """Extrai o texto do documento e envia para a IA com o prompt da skill com validações de tamanho e formato."""
    logger.info(f"Processando arquivo {file.filename} com a skill {skill_name}")
    
    if not file.filename.lower().endswith(".pdf"):
        msg = f"Formato de arquivo inválido ({file.filename}). Apenas documentos em formato PDF (.pdf) são aceitos."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    file_bytes = await file.read()
    
    # Validação de tamanho máximo (50 MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB em bytes
    file_size = len(file_bytes)
    if file_size > MAX_FILE_SIZE:
        file_size_mb = file_size / (1024 * 1024)
        msg = f"O arquivo enviado excede o limite máximo permitido de 50 MB (tamanho enviado: {file_size_mb:.2f} MB)."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )
    
    document_text = extract_text_from_pdf(file_bytes)
    
    skill_instructions = get_skill_prompt(skill_name)
    
    # Montando o prompt final completo (o Gemini 1.5 Flash suporta até 1 milhão de tokens)
    prompt = f"{skill_instructions}\n\nAqui está o conteúdo do documento a ser analisado:\n[DOC_CONTENT]\n{document_text}\n[/DOC_CONTENT]"
    
    # Executando o modelo
    try:
        # Usamos to_thread para não travar o loop do FastAPI
        resultado = await asyncio.to_thread(execute_prompt, prompt)
        return resultado
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Erro na execução da IA: {e}")
        raise HTTPException(status_code=502, detail="Erro ao comunicar com o serviço de IA.")


from datetime import date
from pydantic import BaseModel, Field, field_validator

class ContratoSchema(BaseModel):
    empresa: str | None = Field(None, description="Nome da empresa contratada")
    cnpj: str | None = Field(None, description="CNPJ da empresa contratada")
    data_inicio: date | None = Field(
        None,
        description="Data de início de vigência. Deve ser a data da assinatura digital do contrato (formato YYYY-MM-DD)."
    )
    data_fim: date | None = Field(
        None,
        description="Data de término (fim) de vigência, calculada somando-se a vigencia_prazo em dias à data de início (formato YYYY-MM-DD)."
    )
    vigencia_prazo: int | None = Field(
        None,
        description="Prazo de vigência do contrato em dias (número inteiro positivo maior que zero)."
    )
    valor_contrato: str | None = Field(None, description="Valor do contrato")
    clausula_vigencia: str | None = Field(None, description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes à vigência e prazo.")
    multas_moratorias: str | None = Field(None, description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a multas moratórias por atraso.")
    multas_compensatorias: str | None = Field(None, description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a multas compensatórias.")
    sancoes_administrativas: str | None = Field(None, description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a sanções administrativas.")
    rescisao: str | None = Field(None, description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes às condições de rescisão.")
    numero_contrato: str | None = Field(None, description="Número identificador do contrato (ex: Contrato nº 123/2026, Contrato de Prestação de Serviços nº XXX, etc.)")
    numero_oportunidade: str | None = Field(None, description="Número identificador da oportunidade associada (ex: Oportunidade nº 700xxxxxxx, etc.)")

    @field_validator("vigencia_prazo")
    @classmethod
    def validate_vigencia_prazo(cls, v):
        if v is not None and v <= 0:
            raise ValueError("O prazo de vigência deve ser um número inteiro positivo maior que zero.")
        return v


async def extract_contract_metadata(document_text: str) -> dict:
    """Extrai os metadados do contrato de forma estruturada via LLM com validação de tipos."""
    logger.info("Iniciando extração estruturada de metadados do contrato.")
    
    prompt = (
        "Você é um especialista em análise de contratos. Extraia as seguintes informações do texto do contrato fornecido abaixo:\n"
        "1. Nome da empresa contratada\n"
        "2. CNPJ da empresa contratada\n"
        "3. Data de início do contrato (identifique e utilize a data de assinatura digital do contrato)\n"
        "4. Data de fim do contrato (calcule somando o prazo de vigência em dias à data de início da assinatura digital)\n"
        "5. Prazo de vigência do contrato em dias (número inteiro positivo maior que zero, que preencherá vigencia_prazo)\n"
        "6. Valor do contrato\n"
        "7. Vigência e Prazo (Cópia textual exata e na íntegra das cláusulas de vigência/prazo, que preencherá clausula_vigencia)\n"
        "8. Multas Moratórias (Cópia textual exata e na íntegra das cláusulas de multas moratórias/atraso)\n"
        "9. Multas Compensatórias (Cópia textual exata e na íntegra das cláusulas de multas compensatórias)\n"
        "10. Sanções Administrativas (Cópia textual exata e na íntegra das cláusulas de sanções administrativas)\n"
        "11. Condições de Rescisão (Cópia textual exata e na íntegra das cláusulas de rescisão)\n"
        "12. Número do Contrato (identifique o identificador único do contrato. Procure por termos como 'ICJ XXXXXXX' ou número do contrato principal, ex: '5900.0132964.25.2')\n"
        "13. Número da Oportunidade (identifique o identificador de oportunidade/licitação associado, tipicamente contendo 10 dígitos e iniciando com '700', ex: '7004517339', ou localizado no campo 'Identificação' de relatórios de assinaturas)\n\n"
        "ATENÇÃO: Para as datas de início e fim, retorne no formato padrão AAAA-MM-DD. Para a vigencia_prazo, retorne um número inteiro de dias. Para os itens 7 a 11, você DEVE transcrever literalmente o texto das cláusulas encontradas no contrato, sem resumir ou simplificar o conteúdo.\n\n"
        f"Texto do contrato:\n[DOC_CONTENT]\n{document_text}\n[/DOC_CONTENT]"
    )
    
    try:
        resultado_dict = await asyncio.to_thread(execute_structured_prompt, prompt, ContratoSchema)
        # Validação rígida usando o schema Pydantic para converter datas e inteiro
        validated = ContratoSchema(**resultado_dict)
        return validated.model_dump()
    except Exception as e:
        logger.error(f"Erro na extração estruturada da IA: {e}")
        return {
            "empresa": "Erro na extração",
            "cnpj": "Erro na extração",
            "data_inicio": None,
            "data_fim": None,
            "vigencia_prazo": None,
            "valor_contrato": "Erro na extração",
            "clausula_vigencia": str(e),
            "multas_moratorias": "",
            "multas_compensatorias": "",
            "sancoes_administrativas": "",
            "rescisao": "",
            "numero_contrato": "Erro na extração",
            "numero_oportunidade": "Erro na extração"
        }


def extract_text_from_pdf_with_page_tags(file_bytes: bytes) -> str:
    """Extrai o texto do PDF marcando cada página com [PÁGINA X - TIPO: Y] para permitir que a IA mapeie intervalos."""
    import fitz
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        logger.error(f"Erro ao abrir arquivo PDF para marcação: {e}")
        raise HTTPException(
            status_code=400,
            detail="Erro ao processar o arquivo PDF. Verifique se o arquivo está corrompido ou é inválido."
        )

    text = ""
    for i, page in enumerate(doc):
        has_text = bool(page.get_text().strip())
        has_images = len(page.get_images()) > 0
        if has_text and has_images:
            ptype = "Texto + Imagens"
        elif has_images:
            ptype = "Imagens"
        else:
            ptype = "Texto"
            
        text += f"\n[PÁGINA {i + 1} - TIPO: {ptype}]\n"
        text += page.get_text() + "\n"

    extracted = text.strip()
    return extracted


async def estratificar_contrato(file: UploadFile) -> dict:
    """Processa o documento e gera a estratificação de páginas em JSON estruturado."""
    from models import ReconhecimentoEstratificacaoResponse
    logger.info(f"Iniciando estratificação de layout do arquivo {file.filename}")
    
    if not file.filename.lower().endswith(".pdf"):
        msg = f"Formato de arquivo inválido ({file.filename}). Apenas documentos em formato PDF (.pdf) são aceitos."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    file_bytes = await file.read()
    
    # Validação de tamanho máximo (50 MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    if len(file_bytes) > MAX_FILE_SIZE:
        file_size_mb = len(file_bytes) / (1024 * 1024)
        msg = f"O arquivo enviado excede o limite máximo permitido de 50 MB (tamanho enviado: {file_size_mb:.2f} MB)."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )
        
    document_text_tagged = extract_text_from_pdf_with_page_tags(file_bytes)
    skill_instructions = get_skill_prompt("reconhecimento-estratificacao")
    
    prompt = (
        f"{skill_instructions}\n\n"
        "Aqui está o conteúdo do documento estruturado com marcações de páginas:\n"
        f"[DOC_CONTENT]\n{document_text_tagged}\n[/DOC_CONTENT]"
    )
    
    try:
        resultado_dict = await asyncio.to_thread(
            execute_structured_prompt, prompt, ReconhecimentoEstratificacaoResponse
        )
        validated = ReconhecimentoEstratificacaoResponse(**resultado_dict)
        return validated.model_dump()
    except Exception as e:
        logger.error(f"Erro na execução da estratificação da IA: {e}")
        raise HTTPException(
            status_code=502,
            detail="Erro ao comunicar com o serviço de IA para estratificação."
        )


async def ingestao_metadados_contrato(file: UploadFile) -> dict:
    """Processa o documento e gera a ingestão e extração de metadados cadastrais em JSON estruturado."""
    from models import IngestaoMetadadosSchema
    logger.info(f"Iniciando extração de metadados cadastrais do arquivo {file.filename}")

    if not file.filename.lower().endswith(".pdf"):
        msg = f"Formato de arquivo inválido ({file.filename}). Apenas documentos em formato PDF (.pdf) são aceitos."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    file_bytes = await file.read()

    # Validação de tamanho máximo (50 MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    if len(file_bytes) > MAX_FILE_SIZE:
        file_size_mb = len(file_bytes) / (1024 * 1024)
        msg = f"O arquivo enviado excede o limite máximo permitido de 50 MB (tamanho enviado: {file_size_mb:.2f} MB)."
        logger.warning(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    document_text = extract_text_from_pdf(file_bytes)
    skill_instructions = get_skill_prompt("ingestao-metadados")

    prompt = (
        f"{skill_instructions}\n\n"
        "Aqui está o conteúdo do documento a ser analisado:\n"
        f"[DOC_CONTENT]\n{document_text}\n[/DOC_CONTENT]"
    )

    try:
        resultado_dict = await asyncio.to_thread(
            execute_structured_prompt, prompt, IngestaoMetadadosSchema
        )
        validated = IngestaoMetadadosSchema(**resultado_dict)
        return validated.model_dump()
    except Exception as e:
        logger.error(f"Erro na execução da ingestão de metadados da IA: {e}")
        raise HTTPException(
            status_code=502,
            detail="Erro ao comunicar com o serviço de IA para ingestão de metadados."
        )

