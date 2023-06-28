from sqlalchemy import MetaData, Table, Column, String, Integer, Float, ForeignKey, DateTime

metadata = MetaData()

category = Table(
    "category", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(55), unique=True, nullable=False),
)

product = Table(
    "product", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("owner", String, nullable=False),
    Column("description", String, nullable=True),
    Column("price", Float, nullable=False),
    Column("category", Integer, ForeignKey(category.c.id)),
    # Column("image",),
    Column("created_at", DateTime),
)