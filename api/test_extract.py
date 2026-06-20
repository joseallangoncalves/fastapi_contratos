import sys
import os
import asyncio

# Adiciona o diretório api ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from dotenv import load_dotenv
load_dotenv()

from services.llm_service import extract_contract_metadata

mock_contract_text = """
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

CONTRATANTE: Universidade Federal de Goiás (UFG)
CONTRATADA: Alpha Serviços Terceirizados Ltda, CNPJ: 99.888.777/0001-11

CLÁUSULA PRIMEIRA - DA VIGÊNCIA E PRAZO
1.1. Este contrato entra em vigor na data de sua assinatura, com duração de 24 (vinte e quatro) meses, iniciando-se em 01/07/2026 e encerrando-se em 30/06/2028.

CLÁUSULA SEGUNDA - DO VALOR
2.1. Pela execução dos serviços, a Contratante pagará à Contratada o valor total de R$ 1.200.000,00 (um milhão e duzentos mil reais).

CLÁUSULA TERCEIRA - DAS MULTAS MORATÓRIAS
3.1. Em caso de atraso injustificado no cumprimento das metas pactuadas, aplicar-se-á multa de 0,5% (meio por cento) por dia de atraso, calculada sobre o valor da respectiva parcela mensal.

CLÁUSULA QUARTA - DAS MULTAS COMPENSATÓRIAS
4.1. Pela inexecução total ou parcial do objeto deste contrato, a Contratante poderá aplicar multa compensatória de 10% (dez por cento) sobre o valor total remanescente do contrato.

CLÁUSULA QUINTA - DAS SANÇÕES ADMINISTRATIVAS
5.1. Pelo descumprimento das obrigações contratuais, a Contratada estará sujeita às seguintes sanções:
a) Advertência por escrito;
b) Suspensão temporária de participação em licitação pelo prazo de até 2 (dois) anos.

CLÁUSULA SEXTA - DA RESCISÃO
6.1. O descumprimento de qualquer cláusula autoriza a rescisão de pleno direito, especialmente no caso de atraso na prestação de contas por período superior a 15 dias ou falência da Contratada.
"""

async def test():
    print("Iniciando teste de extração estruturada literal...")
    res = await extract_contract_metadata(mock_contract_text)
    print("\nResultado da extração:")
    for k, v in res.items():
        print(f"\n[{k.upper()}]:")
        print(v)

asyncio.run(test())
