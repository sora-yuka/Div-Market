from sqlalchemy import MetaData, Table, Column, String, Text, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

metadata = MetaData()

category = Table(
    "category", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(55), unique=True, nullable=False),
)

product = Table(
    "product", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("owner", String, nullable=False),
    Column("description", Text, nullable=True),
    Column("price", Float, nullable=False),
    Column("category", Integer, ForeignKey(category.c.id)),
    # Column("image",),
    Column("created_at", DateTime),
)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(55), unique=True, nullable=False)


class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0)
    category = Column(Integer, ForeignKey(category.c.id))
    created_at = Column(DateTime)