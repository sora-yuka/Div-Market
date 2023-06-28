from fastapi import Depends, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from applications.products.models import product, category


#* Category views

async def get_category(session: AsyncSession = Depends(get_async_session)):
    query = select(category)
    result = await session.execute(query)
    return {
        "status": status.HTTP_200_OK,
        "data": [dict(res._mapping) for res in result]
    }

async def create_category(title: str, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(category).values(title=title.lower())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": status.HTTP_201_CREATED,
            "message": "Successfully created"
        }
    except IntegrityError:
        return {
            "status": status.HTTP_403_FORBIDDEN,
            "message": "Category is exists"
        }
    
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(category).where(category.c.id == category_id)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": status.HTTP_204_NO_CONTENT,
        "message": "Category deleted successfully"
    }


#* Product views

async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = select(product)
    result = await session.execute(query)
    return {
        "status": status.HTTP_200_OK,
        "data": [dict(res._mapping) for res in result]
    }
    
async def create_product(product: dict, session: AsyncSession = Depends(get_async_session)):
    return "probka"