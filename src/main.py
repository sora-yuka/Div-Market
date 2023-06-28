from fastapi import FastAPI
from sqladmin import Admin

from config import UserAdmin
from applications.auth import router as auth_router
from applications.profile import router as profile_router
from applications.products import router as product_router
from database import engine


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="Div Market",
    description="Pet project builded on FastAPI",
    version="1.0",
    openapi_url="/openapi.json"
)
# connecting sql-admin panel
admin = Admin(app, engine)
admin.add_view(UserAdmin)

# connecting auth router
app.include_router(auth_router.router, tags=["Auth"])
# connecting profile router
app.include_router(profile_router.router, tags=["Profile"])
# connecting product router
app.include_router(product_router.router, tags=["Product"])