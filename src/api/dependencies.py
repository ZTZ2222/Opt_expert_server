from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import User
from ..utils import get_current_user
from ..database.database import db
from ..database.services import ContentService, CategoryService, SubService, ProductService, UserService, OrderService


async def staff_only(cur_user: User = Depends(get_current_user)):
    if not cur_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    return cur_user


async def admin_only(cur_user: User = Depends(get_current_user)):
    if not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    return cur_user


async def get_content_service(session: AsyncSession = Depends(db.get_session)):
    return ContentService(session)


async def get_category_service(session: AsyncSession = Depends(db.get_session)):
    return CategoryService(session)


async def get_sub_service(session: AsyncSession = Depends(db.get_session)):
    return SubService(session)


async def get_product_service(session: AsyncSession = Depends(db.get_session)):
    return ProductService(session)


async def get_order_service(session: AsyncSession = Depends(db.get_session)):
    return OrderService(session)


async def get_user_service(session: AsyncSession = Depends(db.get_session)):
    return UserService(session)
