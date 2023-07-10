from fastapi import Depends, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from applications.products.models import product, category
from applications.products.schemas import ProductCreate


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
    
async def create_product(product_item: dict, current_user: str, session: AsyncSession = Depends(get_async_session)):
    product_item["owner"] = current_user
    stmt = insert(product).values(**product_item)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": status.HTTP_201_CREATED,
        "message": "Product created successfully",
        "data": product_item,
    }
    
async def detail_product(product_id: int, current_user: str, session: AsyncSession = Depends(get_async_session)):
    query = select(product).where(product.c.id == product_id)
    try:
        result = [dict(res._mapping) for res in await session.execute(query)][0]
    except IndexError:
        return {
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Product doesn't exist"
        }
    return {
        "status": status.HTTP_200_OK,
        "data": result
    }

async def edit_product(product_item: dict, current_user: str, session: AsyncSession = Depends(get_async_session)):
    query = select(product).where(product.c.id == product_item.get("id"))
    try:
        data = [dict(res._mapping) for res in await session.execute(query)][0]
        if data.get("owner") == current_user:
            stmt = (
                update(product).
                where(product.c.id == product_item.get("id")).
                values(**product_item)
            )
            await session.execute(stmt)
            await session.commit()
            return {
                "status": status.HTTP_200_OK,
                "message": "Product has updated successfully",
                "data": [dict(res._mapping) for res in await session.execute(query)][0]
            }
        
        return {
            "status": status.HTTP_403_FORBIDDEN,
            "message": "You aren't product owner",
        }
    except IndexError:
        return {
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Product doesn't exist"
        }