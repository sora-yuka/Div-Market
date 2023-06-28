from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from applications.products import views
from applications.auth import schemas
from utils.token import get_current_user


router = APIRouter(
    prefix="/api/v1/product",
)


@router.get("/category")
async def get_category(session: AsyncSession = Depends(get_async_session)):
    return await views.get_category(session=session)


@router.post("/add_category")
async def create_category(
        title: str, current_user = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)
    ):
    return await views.create_category(title=title, session=session)


@router.delete("/delete_category")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    return await views.delete_category(category_id=category_id, session=session)


@router.get("/product")
async def get_product(current_user = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await views.get_products(session=session)


@router.post("/add_product")
async def create_product(session: AsyncSession = Depends(get_async_session)):
    return "created some product"