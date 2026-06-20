import sys
import os

# Adiciona o diretório api ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from database import Base, engine, SessionLocal
import db_models
from db_models import AnaliseContratualDB

print("Iniciando teste de criação de tabelas e persistência de dados...")

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

# Inicia sessão
db = SessionLocal()

try:
    # 1. Cria uma entrada de teste
    test_entry = AnaliseContratualDB(
        empresa="Empresa de Teste UFG",
        cnpj="12.345.678/0001-90",
        data_inicio="2026-06-19",
        data_fim="2027-06-19",
        valor_contrato="R$ 500.000,00",
        vigencia_prazo="Vigência de 12 meses a partir da assinatura.",
        multas_moratorias="0.1% ao dia em caso de atraso.",
        multas_compensatorias="10% do valor do contrato para descumprimento total.",
        sancoes_administrativas="Advertência por escrito e suspensão temporária.",
        rescisao="Rescisão motivada por inadimplemento por mais de 30 dias."
    )
    db.add(test_entry)
    db.commit()
    db.refresh(test_entry)
    print(f"Sucesso: Entrada inserida com ID {test_entry.id}")

    # 2. Consulta a entrada
    queried = db.query(AnaliseContratualDB).filter(AnaliseContratualDB.id == test_entry.id).first()
    print("Sucesso: Entrada consultada:")
    print(f"  Empresa: {queried.empresa}")
    print(f"  CNPJ: {queried.cnpj}")
    print(f"  Valor: {queried.valor_contrato}")
    print(f"  Data de Inserção: {queried.data_insercao}")

    print("Sucesso: Banco SQLite e SQLAlchemy funcionando perfeitamente.")

finally:
    db.close()
