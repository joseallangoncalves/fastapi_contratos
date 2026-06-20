from fastapi import status, HTTPException
import logging
import os


def get_logger():
    """
    Configura e retorna uma instância do logger da aplicação.

    Returns:
        logging.Logger: Instância do logger configurada com nível INFO
        e formato de mensagem com data/hora, nível e conteúdo.
    """

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("fastapi")

    return logger


def common_api_token(api_token: str):
    """
    Valida o token de autenticação da API.

    Args:
        api_token (str): Token de autenticação fornecido na requisição.

    Raises:
        HTTPException: Retorna status 401 (UNAUTHORIZED) se o token
        fornecido não corresponder ao token configurado na variável
        de ambiente API_TOKEN.

    Returns:
        dict: Dicionário contendo o token validado no formato
        ``{"api_token": api_token}``.
    """
    API_TOKEN = str(os.getenv("API_TOKEN"))
    logger = get_logger()
    logger.info(f"Token recebido: {api_token}")

    if api_token != API_TOKEN:
        logger.warning("Token de autenticação inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
        )

    logger.info("Token de autenticação válido")
import re
import time
from google import genai

# Lista de modelos para fallback (em ordem de preferência)
FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"]


def _extract_retry_delay(error_message: str) -> float:
    """Extrai o tempo de retry sugerido pela API a partir da mensagem de erro."""
    match = re.search(r"Please retry in (\d+(?:\.\d+)?)s", str(error_message))
    if match:
        return float(match.group(1))
    return 0.0


def execute_prompt(prompt: str, model: str = "gemini-2.5-flash", max_retries: int = 5):
    """
    Envia um prompt para o modelo LLM via API do Google Gemini e retorna a resposta.
    Em caso de erro 429 (quota esgotada), tenta modelos alternativos via fallback.
    """
    logger = get_logger()
    logger.info(
        f"Iniciando execução de prompt. Modelo: {model}. (Tamanho do prompt: {len(prompt)} caracteres)"
    )

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Monta lista de modelos: o solicitado primeiro, depois os fallbacks
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]

    for current_model in models_to_try:
        logger.info(f"Tentando modelo: {current_model}")
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=current_model,
                    contents=prompt,
                )

                resultado = response.text
                logger.debug(f"Resposta gerada: {resultado[:500]}...")

                if current_model != model:
                    logger.info(f"Sucesso usando modelo fallback: {current_model}")
                return resultado

            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                logger.warning(
                    f"Erro na tentativa {attempt + 1}/{max_retries} com {current_model}: {e}"
                )

                if is_rate_limit:
                    # Se a quota diária esgotou (limit: 0), pula direto para o próximo modelo
                    if "limit: 0" in error_str:
                        logger.warning(
                            f"Quota diária esgotada para {current_model}. Tentando próximo modelo..."
                        )
                        break  # sai do loop de retries, vai para o próximo modelo

                    # Se é rate limit temporário, respeita o delay sugerido pela API
                    suggested_delay = _extract_retry_delay(error_str)
                    sleep_time = max(suggested_delay + 1, 5 * (attempt + 1))
                else:
                    sleep_time = 5 * (attempt + 1)

                if attempt < max_retries - 1:
                    logger.info(f"Aguardando {sleep_time:.1f}s antes do próximo retry...")
                    time.sleep(sleep_time)
        else:
            # O loop de retries terminou sem sucesso (sem break), mas não esgotou quota diária
            # Tenta o próximo modelo
            continue

    logger.error(f"Falha definitiva em todos os modelos após múltiplas tentativas.")
    return f"[ERRO NA ANÁLISE: Quota esgotada em todos os modelos disponíveis. Aguarde o reset da quota (meia-noite PST) ou ative o billing em https://aistudio.google.com/]"


from typing import Type
from pydantic import BaseModel
from google.genai import types

def execute_structured_prompt(
    prompt: str,
    schema: Type[BaseModel],
    model: str = "gemini-2.5-flash",
    max_retries: int = 5
) -> dict:
    """
    Envia um prompt para o modelo LLM e força o retorno estruturado via JSON Schema.
    Em caso de erro 429, tenta modelos alternativos via fallback.
    Retorna o dicionário com os campos da resposta.
    """
    logger = get_logger()
    logger.info(
        f"Iniciando execução de prompt estruturado. Modelo: {model}. (Tamanho do prompt: {len(prompt)} caracteres)"
    )

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]

    for current_model in models_to_try:
        logger.info(f"Tentando modelo estruturado: {current_model}")
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=current_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                    )
                )

                # response.text é uma string JSON válida
                import json
                try:
                    resultado_dict = json.loads(response.text)
                    return resultado_dict
                except Exception as json_err:
                    logger.error(f"Erro ao fazer parse do JSON retornado: {response.text} - {json_err}")
                    raise json_err

            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                logger.warning(
                    f"Erro na tentativa estruturada {attempt + 1}/{max_retries} com {current_model}: {e}"
                )

                if is_rate_limit:
                    if "limit: 0" in error_str:
                        logger.warning(
                            f"Quota diária esgotada para {current_model}. Tentando próximo modelo estruturado..."
                        )
                        break

                    suggested_delay = _extract_retry_delay(error_str)
                    sleep_time = max(suggested_delay + 1, 5 * (attempt + 1))
                else:
                    sleep_time = 5 * (attempt + 1)

                if attempt < max_retries - 1:
                    logger.info(f"Aguardando {sleep_time:.1f}s antes do próximo retry estruturado...")
                    time.sleep(sleep_time)
        else:
            continue

    logger.error("Falha definitiva estruturada em todos os modelos.")
    raise Exception("Não foi possível obter resposta estruturada do Gemini devido a limite de quota ou erro.")


