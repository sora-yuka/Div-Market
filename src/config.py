from typing import Optional
from sqladmin import Admin, ModelView
from applications.auth.models import User
from applications.products.models import Product
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from decouple import config as conf
from database import engine


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        if username != conf("ADMIN_USERNAME") or password != conf("ADMIN_PASSWORD"):
            return False

        # And update sessio
        request.session.update({"token": "..."})
        
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id, Product.title, Product.price, 
        Product.owner, Product.category, Product.created_at
    ]