from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
import uvicorn
import yaml

# Inicializa o app com docs_url e openapi_url como None para desabilitar o Swagger padrão
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Servir o arquivo YAML
@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse("swagger.yaml")

# Rota para o Swagger UI customizado
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.yaml",
        title="API de Análise de Vagas - Documentação"
    )

# Rota para o ReDoc customizado
@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.yaml",
        title="API de Análise de Vagas - Documentação"
    )

@app.get("/")
async def root():
    return {"message": "API de Análise de Vagas está funcionando!"}

if __name__ == "__main__":
    uvicorn.run("test_api:app", host="0.0.0.0", port=8000, reload=True)