from abc import ABC
from typing import Any, Sequence, Type
from sqlalchemy import insert, select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from . import models
from . import schemas
from ..utils import pwd_context


class Base(ABC):
    model: Type[models.BaseModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _insert(self, **kwargs: Any) -> models.BaseModel:
        async with self.session as session:
            stmt = insert(self.model).values(**kwargs).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def _update(self, *args: Any, **kwargs: Any) -> models.BaseModel:
        async with self.session as session:
            stmt = update(self.model).where(
                *args).values(**kwargs).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
        return result

    async def _select_one(self, *args: Any) -> models.BaseModel:
        async with self.session as session:
            stmt = select(self.model).where(*args)
            result = await session.scalar(stmt)
        return result

    async def _select_all(self) -> Sequence[models.BaseModel]:
        async with self.session as session:
            stmt = select(self.model)
            result = await session.scalars(stmt)
        return result.unique().all()

    async def _delete(self, *args: Any) -> models.BaseModel:
        async with self.session as session:
            stmt = delete(self.model).where(*args).returning(self.model)
            result = await session.scalar(stmt)
            await session.commit()
        return result


class ContentService(Base):
    model = models.Content

    async def create_content(self, content: schemas.ContentCreate) -> models.Content:
        return await self._insert(**content.model_dump(exclude_unset=True, exclude_none=True))

    async def get_content_by_id(self, id: int) -> models.Content:
        return await self._select_one(models.Content.id == id)

    async def get_content_by_title(self, title: str) -> models.Content:
        return await self._select_one(models.Content.title == title)

    async def get_all_content(self) -> Sequence[models.Content]:
        return await self._select_all()

    async def update_content(self, content: schemas.ContentUpdate) -> models.Content:
        content_data = content.model_dump(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.Content.id == content.id, **content_data)

    async def delete_content(self, id: int) -> models.Category:
        return await self._delete(models.Content.id == id)


class CategoryService(Base):
    model = models.Category

    async def create_category(self, category: schemas.CategoryCreate) -> models.Category:
        return await self._insert(**category.model_dump(exclude_unset=True, exclude_none=True))

    async def get_category_by_id(self, id: int) -> models.Category:
        return await self._select_one(models.Category.id == id)

    async def get_category_by_name(self, category_name: str) -> models.Category:
        async with self.session as session:
            stmt = select(models.Category).where(
                models.Category.name == category_name)
            result = await session.scalar(stmt)
        return result

    async def get_all_categories(self) -> list[models.Category]:
        return await self._select_all()

    async def update_category(self, category: schemas.CategoryUpdate) -> models.Category:
        category_data = category.model_dump(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.Category.id == category.id, **category_data)

    async def delete_category(self, id: int) -> models.Category:
        return await self._delete(models.Category.id == id)

    async def get_category_products(self, category_id: int, offset: int, limit: int) -> Any:
        async with self.session as session:
            stmt = select(models.Product).where(
                models.Product.category_id == category_id).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()


class SubService(Base):
    model = models.Sub

    async def create_sub(self, sub: schemas.SubCreate) -> models.Sub:
        return await self._insert(**sub.model_dump(exclude_unset=True, exclude_none=True))

    async def get_sub_by_id(self, id: int) -> models.Sub:
        return await self._select_one(models.Sub.id == id)

    async def get_sub_by_name(self, sub_name: str) -> models.Sub:
        async with self.session as session:
            stmt = select(models.Sub).where(
                models.Sub.name == sub_name)
            result = await session.scalar(stmt)
        return result

    async def get_all_sub(self) -> list[models.Sub]:
        return await self._select_all()

    async def update_sub(self, sub: schemas.CategoryUpdate) -> models.Sub:
        sub_data = sub.model_dump(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.Sub.id == sub.id, **sub_data)

    async def delete_sub(self, id: int) -> models.Sub:
        return await self._delete(models.Sub.id == id)

    async def get_sub_products(self, sub_id: int, offset: int, limit: int) -> Any:
        async with self.session as session:
            stmt = select(models.Product).where(
                models.Product.sub_id == sub_id).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()


class ProductService(Base):
    model = models.Product

    async def create_product(self, product: schemas.ProductCreate) -> models.Product:
        product_insert = await self._insert(**product.model_dump(exclude_unset=True, exclude_none=True, exclude={"inventory"}))

        inventory = product.model_dump(
            exclude_unset=True, exclude_none=True).pop("inventory")
        inventory["product_id"] = product_insert.id
        async with self.session as session:
            stmt = insert(models.Inventory).values(**inventory)
            await session.execute(stmt)
            await session.commit()

        return await self.get_product_by_id(id=product_insert.id)

    async def get_product_by_id(self, id: int) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.id == id).options(
                selectinload(models.Product.inventory))
            result = await session.scalar(stmt)
        return result

    async def get_product_by_name(self, name: str) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.name == name).options(
                selectinload(models.Product.inventory))
            result = await session.scalar(stmt)
        return result

    async def get_product_by_article(self, article: str) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.article == article).options(
                selectinload(models.Product.inventory))
            result = await session.scalar(stmt)
        return result

    async def update_product(self, product: schemas.ProductUpdate) -> models.Product:
        product_data = product.model_dump(
            exclude_unset=True, exclude_none=True)
        updated_product = await self._update(models.Product.id == product.id, **product_data)
        return await self.get_product_by_id(id=updated_product.id)

    async def delete_product(self, id: int) -> models.Product:
        return await self._delete(models.Product.id == id)

    async def get_all_products(self, offset: int, limit: int) -> Sequence[models.Product]:
        async with self.session as session:
            stmt = select(models.Product).options(selectinload(
                models.Product.inventory)).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()


class UserService(Base):
    model = models.User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._password_hasher = pwd_context

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        user.password = self._password_hasher.hash(user.password)
        return await self._insert(**user.model_dump(exclude_unset=True, exclude_none=True))

    async def update_user(self, user: schemas.UserUpdate) -> models.User:
        user.password = user.password
        return await self._update(models.User.id == user.id, **user.model_dump(exclude_unset=True, exclude_none=True))

    async def get_user_by_email(self, email: str) -> models.User:
        return await self._select_one(models.User.email == email)

    async def get_user_by_id(self, id: int) -> models.User:
        return await self._select_one(models.User.id == id)

    async def get_all_users(self) -> Sequence[models.User]:
        return await self._select_all()

    async def delete_user(self, user: schemas.UserUpdate) -> models.User:
        return await self._delete(models.User.id == user.id)

    async def password_change_user(self, user: schemas.UserUpdate) -> models.User:
        payload = {
            "password": self._password_hasher.hash(user.password)}
        return await self._update(models.User.id == user.id, **payload)

    async def grant_admin_privileges(self, user: schemas.UserPrivileges) -> models.User:
        return await self._update(models.User.email == user.email, **user.model_dump())
