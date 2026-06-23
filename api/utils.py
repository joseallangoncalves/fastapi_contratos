from fastapi import status, HTTPException
import logging
import os


def get_logger():
    """
    Configura e retorna uma instância do logger da aplicação.
    Garante que os logs sejam impressos no terminal quando executados no Uvicorn.
    """
    logger = logging.getLogger("fastapi")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = True
    return logger


import re
import time
from google import genai
from google.genai import types
from typing import Type
from pydantic import BaseModel

# Lista de modelos para fallback (em ordem de preferência)
FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"]


def _extract_retry_delay(error_message: str) -> float:
    """Extrai o tempo de retry sugerido pela API a partir da mensagem de erro."""
    match = re.search(r"Please retry in (\d+(?:\.\d+)?)s", str(error_message))
    if match:
        return float(match.group(1))
    return 0.0


def execute_prompt(prompt: str, model: str = "gemini-2.5-flash", max_retries: int = 3):
    """
    Envia um prompt para o modelo LLM via API do Google Gemini e retorna a resposta.
    Em caso de erro 429 (quota esgotada), tenta modelos alternativos via fallback.
    """
    logger = get_logger()
    logger.info(
        f"Iniciando execução de prompt. Modelo: {model}. (Tamanho do prompt: {len(prompt)} caracteres)"
    )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        msg_erro = "Configuração ausente: A chave de API do Gemini (GEMINI_API_KEY) não foi encontrada no arquivo .env."
        logger.error(msg_erro)
        print(f"--> [LOG] ERRO: {msg_erro}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg_erro
        )

    client = genai.Client(api_key=api_key)

    # Monta lista de modelos: o solicitado primeiro, depois os fallbacks
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]

    for current_model in models_to_try:
        logger.info(f"Tentando modelo: {current_model}")
        print(f"--> [LOG] Tentando modelo: {current_model}")
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
                    print(f"--> [LOG] Sucesso usando modelo fallback: {current_model}")
                return resultado

            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                logger.warning(
                    f"Erro na tentativa {attempt + 1}/{max_retries} com {current_model}: {e}"
                )
                print(f"--> [LOG] AVISO: Tentativa {attempt + 1}/{max_retries} de conexão com {current_model} falhou: {e}")

                if is_rate_limit:
                    if "limit: 0" in error_str:
                        logger.warning(
                            f"Quota diária esgotada para {current_model}. Tentando próximo modelo..."
                        )
                        print(f"--> [LOG] AVISO: Quota esgotada para {current_model}. Mudando de modelo...")
                        break  # sai do loop de retries, vai para o próximo modelo

                    suggested_delay = _extract_retry_delay(error_str)
                    sleep_time = max(suggested_delay + 1, 5 * (attempt + 1))
                else:
                    sleep_time = 5 * (attempt + 1)

                if attempt < max_retries - 1:
                    logger.info(f"Aguardando {sleep_time:.1f}s antes do próximo retry...")
                    print(f"--> [LOG] Aguardando {sleep_time:.1f}s para tentar novamente...")
                    time.sleep(sleep_time)
        else:
            # O loop de retries terminou sem sucesso para este modelo, tenta o próximo
            continue

    msg_falha = "Falha definitiva ao conectar à API do Gemini após 3 tentativas. Verifique se a sua chave (GEMINI_API_KEY) no arquivo .env é válida e está ativa, ou se a sua cota de uso diária foi esgotada."
    logger.error(msg_falha)
    print(f"--> [LOG] ERRO: {msg_falha}")
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=msg_falha
    )


def execute_structured_prompt(
    prompt: str,
    schema: Type[BaseModel],
    model: str = "gemini-2.5-flash",
    max_retries: int = 3
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

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        msg_erro = "Configuração ausente: A chave de API do Gemini (GEMINI_API_KEY) não foi encontrada no arquivo .env."
        logger.error(msg_erro)
        print(f"--> [LOG] ERRO: {msg_erro}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg_erro
        )

    client = genai.Client(api_key=api_key)
    models_to_try = [model] + [m for m in FALLBACK_MODELS if m != model]

    for current_model in models_to_try:
        logger.info(f"Tentando modelo estruturado: {current_model}")
        print(f"--> [LOG] Tentando modelo estruturado: {current_model}")
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

                import json
                try:
                    resultado_dict = json.loads(response.text)
                    return resultado_dict
                except Exception as json_err:
                    logger.error(f"Erro ao fazer parse do JSON retornado: {response.text} - {json_err}")
                    print(f"--> [LOG] ERRO: Falha ao fazer parser do JSON da IA: {json_err}")
                    raise json_err

            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                logger.warning(
                    f"Erro na tentativa estruturada {attempt + 1}/{max_retries} com {current_model}: {e}"
                )
                print(f"--> [LOG] AVISO: Tentativa estruturada {attempt + 1}/{max_retries} de conexão com {current_model} falhou: {e}")

                if is_rate_limit:
                    if "limit: 0" in error_str:
                        logger.warning(
                            f"Quota diária esgotada para {current_model}. Tentando próximo modelo estruturado..."
                        )
                        print(f"--> [LOG] AVISO: Quota esgotada estruturada para {current_model}. Mudando de modelo...")
                        break

                    suggested_delay = _extract_retry_delay(error_str)
                    sleep_time = max(suggested_delay + 1, 5 * (attempt + 1))
                else:
                    sleep_time = 5 * (attempt + 1)

                if attempt < max_retries - 1:
                    logger.info(f"Aguardando {sleep_time:.1f}s antes do próximo retry estruturado...")
                    print(f"--> [LOG] Aguardando {sleep_time:.1f}s para tentar novamente...")
                    time.sleep(sleep_time)
        else:
            continue

    msg_falha = "Falha estruturada definitiva ao conectar à API do Gemini após 3 tentativas. Verifique se a sua chave (GEMINI_API_KEY) no arquivo .env é válida e está ativa, ou se a sua cota de uso diária foi esgotada."
    logger.error(msg_falha)
    print(f"--> [LOG] ERRO: {msg_falha}")
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=msg_falha
    )


