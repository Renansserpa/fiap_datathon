
from fastapi import FastAPI
import auth, users, webscrapper
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.get('/')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(webscrapper.router)
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(applications.router)

@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse("swagger.yaml")

app = FastAPI(
    title="API de Análise de Vagas",
    description="API para análise de dados de vagas de emprego",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.yaml"
)