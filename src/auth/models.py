from sqlalchemy import (
    Table, MetaData, Column, String, Integer, Float, Boolean, Sequence, DateTime
)

metadata = MetaData()

account = Table(
    "account", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("username", String(75), nullable=False),
    Column("hashed_password", String(125), nullable=False),
    Column("balance", Float, default="0"),
    Column("created_at", DateTime),
    Column("is_active", Boolean, default=False),
)