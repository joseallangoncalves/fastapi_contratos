"""
Biblioteca Python para a API Aula - Construção de APIs para IA.

Encapsula todos os endpoints definidos no openapi.json, oferecendo uma
interface simples e intuitiva sem expor detalhes internos da API.

Exemplo de uso::

    from biblioteca_api import BibliotecaAPI

    api = BibliotecaAPI(base_url="http://localhost:8000", api_token="meu-token")

    # Gerar uma história
    resultado = api.gerar_historia(tema="aventura no espaço")

    # Realizar uma operação matemática
    resultado = api.operacao_matematica(operacao="soma", numero1=10, numero2=5)
"""

import warnings

import requests


class BibliotecaAPI:
    """
    Cliente Python para a API Aula.

    Args:
        base_url: URL base da API (ex: ``"http://localhost:8000"``).
        api_token: Token de autenticação exigido por todos os endpoints.
    """

    def __init__(self, base_url: str, api_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._session = requests.Session()

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _post(
        self, path: str, params: dict | None = None, json: dict | None = None
    ) -> dict:
        params = params or {}
        params["api_token"] = self.api_token
        response = self._session.post(
            f"{self.base_url}{path}", params=params, json=json
        )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # IA
    # ------------------------------------------------------------------

    def gerar_historia(self, tema: str) -> dict:
        """Gera uma história com base em um tema usando IA.

        Args:
            tema: O tema da história a ser gerada.

        Returns:
            Resposta da API com a história gerada.
        """
        return self._post("/gerar_historia/v1", json={"tema": tema})["historia"]

    # ------------------------------------------------------------------
    # Operações matemáticas
    # ------------------------------------------------------------------

    def soma_v1(self, numero1: int, numero2: int) -> dict:
        """Soma dois números via parâmetros de caminho (path params).

        .. deprecated::
            Este endpoint será descontinuado em 15/06.
            Prefira :meth:`soma_v2` ou :meth:`soma_v3`.

        Args:
            numero1: Primeiro número.
            numero2: Segundo número.

        Returns:
            Resposta da API com o resultado da soma.
        """
        warnings.warn(
            "soma_v1() está depreciado e será descontinuado em 15/06. "
            "Use soma_v2() ou soma_v3() em seu lugar.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._post(f"/soma/v1/{numero1}/{numero2}")

    def soma_v2(self, numero1: int, numero2: int) -> dict:
        """Soma dois números via parâmetros de query.

        Args:
            numero1: Primeiro número.
            numero2: Segundo número.

        Returns:
            Resposta da API com o resultado da soma.
        """
        return self._post("/soma/v2", params={"numero1": numero1, "numero2": numero2})

    def soma_v3(self, numero1: int = 5, numero2: int = 3) -> dict:
        """Soma dois números enviados via corpo da requisição (request body).

        Args:
            numero1: Primeiro número (padrão: ``5``).
            numero2: Segundo número (padrão: ``3``).

        Returns:
            ``dict`` com a chave ``"resultado"`` contendo o valor da soma.
        """
        return self._post("/soma/v3", json={"numero1": numero1, "numero2": numero2})

    def operacao_matematica(
        self,
        operacao: str,
        numero1: int = 5,
        numero2: int = 3,
    ) -> dict:
        """Realiza uma operação matemática entre dois números.

        Args:
            operacao: Tipo de operação. Valores válidos:
                ``"soma"``, ``"subtracao"``, ``"multiplicacao"``, ``"divisao"``.
            numero1: Primeiro número (padrão: ``5``).
            numero2: Segundo número (padrão: ``3``).

        Returns:
            Resposta da API com o resultado da operação.

        Raises:
            ValueError: Se ``operacao`` não for um dos valores aceitos.
        """
        operacoes_validas = {"soma", "subtracao", "multiplicacao", "divisao"}
        if operacao not in operacoes_validas:
            raise ValueError(
                f"Operação inválida: '{operacao}'. "
                f"Valores aceitos: {sorted(operacoes_validas)}"
            )
        return self._post(
            "/operacao_matematica/v1",
            params={"operacao": operacao},
            json={"numero1": numero1, "numero2": numero2},
        )
