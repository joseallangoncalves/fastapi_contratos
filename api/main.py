from fastapi import FastAPI, Depends

from dotenv import load_dotenv, find_dotenv
from routers.health_router import router as health_router
from routers.auth_router import get_current_active_user, router as auth_router
from routers.contratos_router import router as contratos_router
from fastapi_mcp import FastApiMCP


from database import Base, engine
import db_models

Base.metadata.create_all(bind=engine)

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
    tags=["Análise de Contratos (IA)"],
    dependencies=[Depends(get_current_active_user)],
)

mcp = FastApiMCP(app)
mcp.mount_http()
