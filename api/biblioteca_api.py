"""
Biblioteca Python para a API de Análise de Contratos.

Encapsula todos os endpoints definidos na API de análise de contratos,
permitindo realizar análises contratuais, extrair obrigações de SMS e
gerar checklists de verificação.

Exemplo de uso::

    from biblioteca_api import BibliotecaAPI

    # Inicializa o cliente
    api = BibliotecaAPI(base_url="http://localhost:8000")

    # Faz o login para obter o token JWT
    api.login(username="johndoe", password="secret")

    # Envia um contrato para análise
    resultado = api.analise_contratual("caminho/para/contrato.pdf")
    print(resultado["analise"])
"""

import requests
from typing import Dict, Any, List


class BibliotecaAPI:
    """
    Cliente Python para a API de Análise de Contratos.

    Args:
        base_url: URL base da API (ex: ``"http://localhost:8000"``).
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token: str | None = None
        self._session = requests.Session()

    def login(self, username: str, password: str) -> str:
        """Autentica na API e armazena o token JWT.

        Args:
            username: Nome de usuário.
            password: Senha de acesso.

        Returns:
            O token JWT gerado.
        """
        response = self._session.post(
            f"{self.base_url}/api/v1/token",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return self.token

    def _get_headers(self) -> dict:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _post_file(self, path: str, file_path: str) -> dict:
        headers = self._get_headers()
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            response = self._session.post(
                f"{self.base_url}{path}", headers=headers, files=files
            )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Endpoints de IA (Análise de Contratos)
    # ------------------------------------------------------------------

    def analise_contratual(self, file_path: str) -> dict:
        """Envia um contrato em PDF para analisar multas, penalidades e vigência.

        Args:
            file_path: Caminho local para o arquivo PDF do contrato.

        Returns:
            Resposta da API com o ID da análise, relatório markdown e dados salvos.
        """
        return self._post_file("/api/v1/contratos/analise-contratual", file_path)

    def analise_sms(self, file_path: str) -> dict:
        """Extrai obrigações de Saúde, Segurança e Meio Ambiente (SMS) do contrato.

        Args:
            file_path: Caminho local para o arquivo PDF do contrato.

        Returns:
            Resposta contendo o relatório de SMS gerado pela IA.
        """
        return self._post_file("/api/v1/contratos/analise-sms", file_path)

    def gerar_checklist(self, file_path: str) -> dict:
        """Gera um checklist estruturado para apoiar a fiscalização do contrato.

        Args:
            file_path: Caminho local para o arquivo PDF do contrato.

        Returns:
            Resposta contendo o checklist gerado em formato Markdown.
        """
        return self._post_file("/api/v1/contratos/gerar-checklist", file_path)

    # ------------------------------------------------------------------
    # Consultas ao Banco de Dados
    # ------------------------------------------------------------------

    def listar_analises(self, empresa: str | None = None, cnpj: str | None = None) -> List[dict]:
        """Consulta as análises contratuais salvas no banco de dados.

        Args:
            empresa: Filtro por nome de empresa (busca parcial).
            cnpj: Filtro por CNPJ exato.

        Returns:
            Lista de análises encontradas.
        """
        headers = self._get_headers()
        params = {}
        if empresa:
            params["empresa"] = empresa
        if cnpj:
            params["cnpj"] = cnpj

        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/analises", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def obter_analise(self, id_analise: int) -> dict:
        """Recupera os detalhes completos de uma análise específica por ID.

        Args:
            id_analise: ID do registro no banco de dados.

        Returns:
            Dados e relatórios completos da análise.
        """
        headers = self._get_headers()
        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/analises/{id_analise}", headers=headers
        )
        response.raise_for_status()
        return response.json()
