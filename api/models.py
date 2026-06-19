from pydantic import BaseModel, Field
from enum import Enum


class Numeros(BaseModel):
    numero1: int = Field(5, description="O primeiro número a ser somado")
    numero2: int = Field(3, description="O segundo número a ser somado")


class Resultado(BaseModel):
    resultado: int = Field(..., description="O resultado da soma dos dois números")


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


class Historia(BaseModel):
    tema: str = Field(..., description="O tema da história a ser gerada")


class WebSearchRequest(BaseModel):
    query: str = Field(..., description="A consulta de busca a ser realizada")
    max_results: int = Field(
        10, description="O número máximo de resultados a serem retornados"
    )
    region: str = Field(
        "pt-br", description="A região para a busca, por exemplo, 'pt-br' para Brasil"
    )


class WebSearchResult(BaseModel):
    date: str = Field(..., description="A data da notícia")
    title: str = Field(..., description="O título da notícia")
    body: str = Field(..., description="O corpo da notícia")
    url: str = Field(..., description="A URL da notícia")
    image: str = Field(..., description="A URL da imagem associada à notícia")
    source: str = Field(..., description="A fonte da notícia")


class WebSearchResults(BaseModel):
    results: list[WebSearchResult] = Field(
        ..., description="A lista de resultados da busca"
    )


class ExtractURLRequest(BaseModel):
    url: str = Field(..., description="A URL da qual o conteúdo deve ser extraído")


class ExtractURLResponse(BaseModel):
    url: str = Field(..., description="A URL da qual o conteúdo foi extraído")
    content: str = Field(..., description="O conteúdo extraído da URL")


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
