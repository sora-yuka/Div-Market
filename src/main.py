from fastapi import FastAPI
from applications.auth import router as auth_router
from applications.profile import router as profile_router

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Div Market",
    description="Pet project builded on FastAPI",
    version="1.0",
    openapi_url="/openapi.json"
)

# connecting auth router
app.include_router(auth_router.router, tags=["Auth"])
# connecting profile router
app.include_router(profile_router.router, tags=["Profile"])