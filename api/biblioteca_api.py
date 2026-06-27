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

    def reconhecimento_estratificacao(self, file_path: str) -> dict:
        """Mapeia os intervalos de páginas de cada seção do contrato e extrai seu número.

        Args:
            file_path: Caminho local para o arquivo PDF do contrato.

        Returns:
            Resposta contendo o número do contrato e intervalos de páginas das seções.
        """
        return self._post_file("/api/v1/contratos/reconhecimento-estratificacao", file_path)

    def ingestao_metadados(self, file_path: str) -> dict:
        """Extrai os metadados cadastrais principais (objeto, contratante, contratada, prazos e valor) e os salva no banco de dados.

        Args:
            file_path: Caminho local para o arquivo PDF do contrato.

        Returns:
            Resposta contendo os metadados cadastrais extraídos e persistidos.
        """
        return self._post_file("/api/v1/contratos/ingestao-metadados", file_path)

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

    def listar_estratificacoes(self, numero_contrato: str | None = None) -> List[dict]:
        """Consulta as estratificações de páginas de contratos salvas no banco de dados.

        Args:
            numero_contrato: Filtro por número identificador do contrato.

        Returns:
            Lista de estratificações encontradas.
        """
        headers = self._get_headers()
        params = {}
        if numero_contrato:
            params["numero_contrato"] = numero_contrato

        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/reconhecimento-estratificacao", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def obter_estratificacao(self, id_estratificacao: int) -> dict:
        """Recupera os detalhes de uma estratificação de páginas por ID.

        Args:
            id_estratificacao: ID do registro de estratificação no banco.

        Returns:
            Dados de estratificação de páginas do contrato.
        """
        headers = self._get_headers()
        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/reconhecimento-estratificacao/{id_estratificacao}", headers=headers
        )
        response.raise_for_status()
        return response.json()

    def listar_metadados(self, numero_contrato: str | None = None, contratada: str | None = None) -> List[dict]:
        """Consulta os registros de metadados cadastrais persistidos.

        Args:
            numero_contrato: Filtro por número de contrato.
            contratada: Filtro por nome da empresa contratada.

        Returns:
            Lista de registros de metadados encontrados.
        """
        headers = self._get_headers()
        params = {}
        if numero_contrato:
            params["numero_contrato"] = numero_contrato
        if contratada:
            params["contratada"] = contratada

        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/ingestao-metadados", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def obter_metadados(self, id_metadados: int) -> dict:
        """Recupera os detalhes de um registro específico de metadados cadastrais por ID.

        Args:
            id_metadados: ID do registro de metadados cadastrais no banco.

        Returns:
            Metadados cadastrais do contrato.
        """
        headers = self._get_headers()
        response = self._session.get(
            f"{self.base_url}/api/v1/contratos/ingestao-metadados/{id_metadados}", headers=headers
        )
        response.raise_for_status()
        return response.json()
