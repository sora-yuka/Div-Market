from fastapi import FastAPI
from auth import router as auth_router


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Div Market",
    description="Pet project builded on FastAPI",
    version="1.0",
    openapi_url="/openapi.json"
)

app.include_router(auth_router.router, tags=["Auth"])