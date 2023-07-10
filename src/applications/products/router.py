from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from applications.products import views
from applications.products import schemas
from utils.token import get_current_user


router = APIRouter(
    prefix="/api/v1/product",
)


@router.get("/category/")
async def get_category(session: AsyncSession = Depends(get_async_session)):
    """ Getting category list """
    return await views.get_category(session=session)


@router.post("/add_category/")
async def create_category(
        title: str, current_user = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)
    ):
    """ Creating category for product """
    return await views.create_category(title=title, session=session)


@router.delete("/delete_category/")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    """ Deleting category """
    return await views.delete_category(category_id=category_id, session=session)


@router.get("/")
async def get_product(current_user = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    """ Getting product list """
    return await views.get_products(session=session)


@router.get("/detail/")
async def detail_product(
        product_id: int, current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Getting detailed product """
    return await views.detail_product(product_id=product_id, current_user=current_user, session=session)


@router.post("/add_product/")
async def create_product(
        product: schemas.ProductCreate, current_user = Depends(get_current_user), 
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Creating product """
    return await views.create_product(product_item=product.dict(), current_user=current_user, session=session)


@router.patch("/edit/")
async def edit_product(
        product: schemas.ProductEdit, current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Editing product """
    return await views.edit_product(product_item=product.dict(), current_user=current_user, session=session)