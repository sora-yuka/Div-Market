from sqladmin import Admin, ModelView
from applications.auth.models import User
from database import engine


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
