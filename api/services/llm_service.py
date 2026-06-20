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
    """Extrai texto de um arquivo PDF usando PyMuPDF (fitz)."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        raise HTTPException(status_code=400, detail="Erro ao processar o arquivo PDF. Verifique se o arquivo é válido.")


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
    """Extrai o texto do documento e envia para a IA com o prompt da skill."""
    logger.info(f"Processando arquivo {file.filename} com a skill {skill_name}")
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são suportados no momento.")

    file_bytes = await file.read()
    
    document_text = extract_text_from_pdf(file_bytes)
    if not document_text:
        raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF fornecido.")
    
    skill_instructions = get_skill_prompt(skill_name)
    
    # Montando o prompt final completo (o Gemini 1.5 Flash suporta até 1 milhão de tokens)
    prompt = f"{skill_instructions}\n\nAqui está o conteúdo do documento a ser analisado:\n[DOC_CONTENT]\n{document_text}\n[/DOC_CONTENT]"
    
    # Executando o modelo
    try:
        # Usamos to_thread para não travar o loop do FastAPI
        resultado = await asyncio.to_thread(execute_prompt, prompt)
        return resultado
    except Exception as e:
        logger.error(f"Erro na execução da IA: {e}")
        raise HTTPException(status_code=502, detail="Erro ao comunicar com o serviço de IA.")


from pydantic import BaseModel, Field

class ContratoSchema(BaseModel):
    empresa: str = Field(description="Nome da empresa contratada")
    cnpj: str = Field(description="CNPJ da empresa contratada")
    data_inicio: str = Field(description="Data de início do contrato")
    data_fim: str = Field(description="Data de fim do contrato")
    valor_contrato: str = Field(description="Valor do contrato")
    vigencia_prazo: str = Field(description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes à vigência e prazo.")
    multas_moratorias: str = Field(description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a multas moratórias por atraso.")
    multas_compensatorias: str = Field(description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a multas compensatórias.")
    sancoes_administrativas: str = Field(description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes a sanções administrativas.")
    rescisao: str = Field(description="Cópia ou transcrição exata e na íntegra das cláusulas do contrato referentes às condições de rescisão.")


async def extract_contract_metadata(document_text: str) -> dict:
    """Extrai os metadados do contrato de forma estruturada via LLM."""
    logger.info("Iniciando extração estruturada de metadados do contrato.")
    
    prompt = (
        "Você é um especialista em análise de contratos. Extraia as seguintes informações do texto do contrato fornecido abaixo:\n"
        "1. Nome da empresa contratada\n"
        "2. CNPJ da empresa contratada\n"
        "3. Data de início do contrato\n"
        "4. Data de fim do contrato\n"
        "5. Valor do contrato\n"
        "6. Vigência e Prazo (Cópia textual exata e na íntegra das cláusulas de vigência/prazo)\n"
        "7. Multas Moratórias (Cópia textual exata e na íntegra das cláusulas de multas moratórias/atraso)\n"
        "8. Multas Compensatórias (Cópia textual exata e na íntegra das cláusulas de multas compensatórias)\n"
        "9. Sanções Administrativas (Cópia textual exata e na íntegra das cláusulas de sanções administrativas)\n"
        "10. Condições de Rescisão (Cópia textual exata e na íntegra das cláusulas de rescisão)\n\n"
        "ATENÇÃO: Para os itens 6 a 10, você DEVE transcrever literalmente o texto das cláusulas encontradas no contrato, sem resumir ou simplificar o conteúdo.\n\n"
        f"Texto do contrato:\n[DOC_CONTENT]\n{document_text}\n[/DOC_CONTENT]"
    )
    
    try:
        resultado_dict = await asyncio.to_thread(execute_structured_prompt, prompt, ContratoSchema)
        return resultado_dict
    except Exception as e:
        logger.error(f"Erro na extração estruturada da IA: {e}")
        # Retorna campos vazios para não impedir o fluxo principal caso dê erro na extração
        return {
            "empresa": "Erro na extração",
            "cnpj": "Erro na extração",
            "data_inicio": "Erro na extração",
            "data_fim": "Erro na extração",
            "valor_contrato": "Erro na extração",
            "vigencia_prazo": str(e),
            "multas_moratorias": "",
            "multas_compensatorias": "",
            "sancoes_administrativas": "",
            "rescisao": ""
        }

