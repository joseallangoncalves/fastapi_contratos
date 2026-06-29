from fastapi import FastAPI, Depends

from dotenv import load_dotenv, find_dotenv
from routers.health_router import router as health_router
from routers.auth_router import get_current_active_user, router as auth_router
from routers.contratos_router import router as contratos_router
from fastapi_mcp import FastApiMCP


from database import Base, engine
import db_models

Base.metadata.create_all(bind=engine)

# Migração automática das novas colunas para SQLite
from sqlalchemy import inspect, text

inspector = inspect(engine)
try:
    columns = [col["name"] for col in inspector.get_columns("analises_contratuais")]
    with engine.begin() as conn:
        if "numero_contrato" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE analises_contratuais ADD COLUMN numero_contrato VARCHAR"
                )
            )
        if "numero_oportunidade" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE analises_contratuais ADD COLUMN numero_oportunidade VARCHAR"
                )
            )

    # Migração para a tabela reconhecimento_estratificacao
    columns_strat = [
        col["name"] for col in inspector.get_columns("reconhecimento_estratificacao")
    ]
    with engine.begin() as conn:
        for suffix in [
            "relatorio_assinatura",
            "instrumento_contratual_icj",
            "especificacao_tecnica_memorial",
            "planilha_precos_ppu",
            "anexo_sms",
            "circulares_conformidade",
        ]:
            col_name = f"{suffix}_tipo"
            if col_name not in columns_strat:
                conn.execute(
                    text(
                        f"ALTER TABLE reconhecimento_estratificacao ADD COLUMN {col_name} VARCHAR"
                    )
                )
except Exception as e:
    print(f"--> [MIGRATION WARNING] Erro na migração das novas colunas: {e}")

load_dotenv(find_dotenv(), override=True)


app = FastAPI(
    title="API de Análise de Contratos",
    description="API que disponibiliza endpoints de Inteligência Artificial para extração e análise de informações em documentos contratuais.",
    summary="Trabalho final da disciplina de Construção de APIs para IA",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "José Allan - Elson - PH - Geiziane",
        "url": "https://github.com/joseallangoncalves/fastapi_contratos",
        "email": "joseallan@ufg.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Inclusão das rotas (endpoints)
app.include_router(router=health_router, prefix="/api/v1", tags=["Health Check"])
app.include_router(router=auth_router, prefix="/api/v1", tags=["Autenticação"])
app.include_router(
    router=contratos_router,
    prefix="/api/v1/contratos",
    dependencies=[Depends(get_current_active_user)],
)

mcp = FastApiMCP(app)
mcp.mount_http()
