from sqlalchemy import (
    Table, MetaData, Column, String, Integer, Float, Boolean, DateTime
)
from database import Base


metadata = MetaData()

account = Table(
    "account", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("username", String(75), nullable=False),
    Column("hashed_password", String(125), nullable=False),
    Column("balance", Float, default=0),
    # Column("role"),
    Column("created_at", DateTime),
    Column("is_active", Boolean, default=False),
    Column("activation_code", String, nullable=True),
)

code = Table(
    "recovery_code", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("code", Integer, unique=True, nullable=True),
)


class User(Base):
    __tablename__ = "account"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    balance = Column(Float, default=0)
    # role = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=75), nullable=False)
    created_at = Column(DateTime)