from abc import ABC
from typing import Any, Sequence, Type
from slugify import slugify
from sqlalchemy import insert, select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from . import models
from . import schemas
from ..utils import pwd_context, upload_category_image, upload_content_image, upload_product_images


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
        return await self._insert(**content.dict(exclude_unset=True, exclude_none=True))

    async def get_content_by_id(self, id: int) -> models.Content:
        return await self._select_one(models.Content.id == id)

    async def get_content_by_title(self, title: str) -> models.Content:
        return await self._select_one(models.Content.title == title)

    async def get_all_content(self) -> Sequence[models.Content]:
        return await self._select_all()

    async def update_content(self, content: schemas.ContentUpdate) -> models.Content:
        content_data = content.dict(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.Content.id == content.id, **content_data)

    async def delete_content(self, id: int) -> models.Category:
        return await self._delete(models.Content.id == id)


class CategoryService(Base):
    model = models.Category

    async def create_category(self, category: schemas.CategoryCreate) -> models.Category:
        if category.image:
            category.image = upload_category_image(category.image)

        category.slug_en = slugify(category.name)

        async with self.session as session:
            stmt = insert(models.RouteMapping).values(
                slug_en=category.slug_en, name=category.name)
            await session.execute(stmt)
            await session.commit()
        return await self._insert(**category.dict(exclude_unset=True, exclude_none=True))

    async def get_category_by_id(self, id: int) -> models.Category:
        return await self._select_one(models.Category.id == id)

    async def get_category_by_slug(self, category_slug: str) -> models.Category:
        async with self.session as session:
            stmt = select(models.Category).where(
                models.Category.slug_en == category_slug)
            result = await session.scalar(stmt)
        return result

    async def get_all_categories(self) -> list[models.Category]:
        return await self._select_all()

    async def update_category(self, category: schemas.CategoryUpdate) -> models.Category:
        category.slug_en = slugify(category.name)

        if category.image.startswith("data:image"):
            image_url = upload_category_image(category.image)
            category.image = image_url

        async with self.session as session:
            stmt = insert(models.RouteMapping).values(
                slug_en=category.slug_en, name=category.name)
            await session.execute(stmt)
            await session.commit()

        category_data = category.dict(exclude_unset=True, exclude_none=True)
        return await self._update(models.Category.id == category.id, **category_data)

    async def delete_category(self, id: int) -> models.Category:
        return await self._delete(models.Category.id == id)

    async def get_category_products(self, category_id: int, offset: int, limit: int) -> list[models.Product]:
        async with self.session as session:
            stmt = select(models.Product).where(
                models.Product.category_id == category_id).options(
                selectinload(models.Product.category),
                selectinload(models.Product.sub)).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()


class SubService(Base):
    model = models.Sub

    async def create_sub(self, sub: schemas.SubCreate) -> models.Sub:
        return await self._insert(**sub.dict(exclude_unset=True, exclude_none=True))

    async def get_sub_by_id(self, id: int) -> models.Sub:
        return await self._select_one(models.Sub.id == id)

    async def get_sub_by_name(self, sub_name: str) -> models.Sub:
        async with self.session as session:
            stmt = select(models.Sub).where(models.Sub.name == sub_name)
            result = await session.scalar(stmt)
        return result

    async def get_all_sub(self) -> list[models.Sub]:
        return await self._select_all()

    async def update_sub(self, sub: schemas.CategoryUpdate) -> models.Sub:
        sub_data = sub.dict(
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
        if product.images:
            product.images = upload_product_images(product.images)
        product.slug_en = slugify(product.name)
        product_insert = await self._insert(**product.dict(exclude_unset=True, exclude_none=True))

        return await self.get_product_by_id(id=product_insert.id)

    async def get_product_by_id(self, id: int) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.id == id).options(
                selectinload(models.Product.category),
                selectinload(models.Product.sub))
            result = await session.scalar(stmt)
        return result

    async def get_product_by_slug(self, slug: str) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.slug_en == slug).options(
                selectinload(models.Product.category),
                selectinload(models.Product.sub))
            result = await session.scalar(stmt)
        return result

    async def get_product_by_article(self, article: str) -> models.Product:
        async with self.session as session:
            stmt = select(models.Product).where(models.Product.article == article).options(
                selectinload(models.Product.category),
                selectinload(models.Product.sub))
            result = await session.scalar(stmt)
        return result

    async def update_product(self, product: schemas.ProductUpdate) -> models.Product:
        product.slug_en = slugify(product.name)
        if any(image.startswith("data:image") for image in product.images):
            image_urls = upload_product_images(product.images)
            product.images = image_urls
        product_data = product.dict(exclude_unset=True, exclude_none=True)
        updated_product = await self._update(models.Product.id == product.id, **product_data)

        return await self.get_product_by_id(id=updated_product.id)

    async def delete_product(self, id: int) -> None:
        async with self.session as session:
            # Delete the product
            await session.execute(delete(models.Product).where(models.Product.id == id))
            await session.commit()

    async def get_all_products(self, offset: int, limit: int, search_query: str = None) -> Sequence[models.Product]:
        async with self.session as session:
            stmt = select(models.Product).options(
                selectinload(models.Product.category),
                selectinload(models.Product.sub)
            ).offset(offset).limit(limit)

            if search_query:
                stmt = stmt.where(
                    models.Product.name.ilike(f"%{search_query}%"))

            result = await session.scalars(stmt)
        return result.all()


class UserService(Base):
    model = models.User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._password_hasher = pwd_context

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        user.password = self._password_hasher.hash(user.password)
        return await self._insert(**user.dict(exclude_unset=True, exclude_none=True))

    async def update_user(self, user: schemas.UserUpdate) -> models.User:
        user.password = self._password_hasher.hash(user.password)
        return await self._update(models.User.id == user.id, **user.dict(exclude_unset=True, exclude_none=True))

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


class OrderService(Base):
    model = models.Order

    async def create_order(self, order: schemas.OrderCreate) -> models.Order:
        new_order = await self._insert(**order.dict(exclude_unset=True, exclude_none=True, exclude={"items"}))
        items = order.dict(
            exclude_unset=True, exclude_none=True).get("items")

        for item in items:
            item["order_id"] = new_order.id
            async with self.session as session:
                stmt = insert(models.OrderItem).values(**item)
                await session.execute(stmt)
                await session.commit()

        return await self.get_order_by_id(id=new_order.id)

    async def get_order_by_id(self, id: int) -> models.Order:
        async with self.session as session:
            stmt = select(models.Order).where(models.Order.id ==
                                              id).options(selectinload(models.Order.items))
            result = await session.scalar(stmt)
        return result

    async def return_order(self, order: schemas.OrderUpdate) -> models.Order:
        order_data = order.dict(exclude_unset=True, exclude_none=True)
        order_data["status"] = "returned"
        updated_order = await self._update(models.Order.id == order.id, **order_data)
        return await self.get_order_by_id(id=updated_order.id)

    async def update_order_info(self, order: schemas.OrderUpdate) -> models.Order:
        async with self.session as session:
            order_data = order.dict(
                exclude_unset=True, exclude_none=True, exclude={"items"})
            stmt = update(models.Order).where(
                models.Order.id == order.id).values(**order_data)
            await session.execute(stmt)
            await session.commit()

        return await self.get_order_by_id(id=order.id)

    async def delete_order(self, id: int) -> None:
        return await self._delete(models.Order.id == id)

    async def get_customer_orders(self, phone_numb: str) -> Sequence[models.Order]:
        async with self.session as session:
            stmt = select(models.Order).where(
                models.Order.telephone == phone_numb)
            result = await session.scalars(stmt)
        return result.all()

    async def get_all_orders(self, offset: int, limit: int) -> Sequence[models.Order]:
        async with self.session as session:
            stmt = select(models.Order).options(selectinload(
                models.Order.items)).offset(offset).limit(limit)
            result = await session.scalars(stmt)
        return result.all()


class RequestItemService(Base):
    model = models.RequestItem

    async def create_request_item(self, request_item: schemas.RequestItemCreate) -> models.RequestItem:
        return await self._insert(**request_item.dict(exclude_unset=True, exclude_none=True))

    async def get_request_item_by_id(self, id: int) -> models.RequestItem:
        return await self._select_one(models.RequestItem.id == id)

    async def get_request_item_by_name(self, request_item_name: str) -> models.RequestItem:
        async with self.session as session:
            stmt = select(models.RequestItem).where(
                models.RequestItem.name == request_item_name)
            result = await session.scalar(stmt)
        return result

    async def get_all_request_items(self) -> list[models.RequestItem]:
        return await self._select_all()

    async def delete_request_item(self, id: int) -> models.RequestItem:
        return await self._delete(models.RequestItem.id == id)


class SizeService(Base):
    model = models.Size

    async def create_size(self, size: schemas.SizeCreate) -> models.Size:
        return await self._insert(**size.dict(exclude_unset=True, exclude_none=True))

    async def get_size_by_id(self, id: int) -> models.Size:
        return await self._select_one(models.Size.id == id)

    async def get_all_sizes(self) -> list[models.Size]:
        return await self._select_all()

    async def delete_size(self, id: int) -> models.Size:
        return await self._delete(models.Size.id == id)


class PageContentService(Base):
    model = models.PageContent

    async def create_page_content(self, content: schemas.PageContentCreate) -> models.PageContent:
        if content.backgroundImage:
            content.backgroundImage = upload_content_image(
                content.backgroundImage)
        return await self._insert(**content.dict(exclude_unset=True, exclude_none=True))

    async def get_page_content_by_id(self, id: int) -> models.PageContent:
        return await self._select_one(models.PageContent.id == id)

    async def get_page_content_by_title(self, title: str) -> models.PageContent:
        return await self._select_one(models.PageContent.title == title)

    async def get_all_page_content(self) -> Sequence[models.PageContent]:
        return await self._select_all()

    async def update_page_content(self, content: schemas.PageContentUpdate) -> models.PageContent:
        if content.backgroundImage.startswith("data:image"):
            image_url = upload_content_image(content.backgroundImage)
            content.backgroundImage = image_url
        content_data = content.dict(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.PageContent.id == content.id, **content_data)

    async def delete_page_content(self, id: int) -> models.Category:
        return await self._delete(models.PageContent.id == id)


class RouteMappingService(Base):
    model = models.RouteMapping

    async def create_route_mapping(self, route_mapping: schemas.RouteMapping) -> models.RouteMapping:
        return await self._insert(**route_mapping.dict(exclude_unset=True, exclude_none=True))

    async def update_route_mapping(self, route_mapping: schemas.RouteMapping) -> models.RouteMapping:
        route_mapping_data = route_mapping.dict(
            exclude_unset=True, exclude_none=True)
        return await self._update(models.RouteMapping.id == route_mapping.id, **route_mapping_data)

    async def delete_route_mapping(self, id: int) -> None:
        return await self._delete(models.RouteMapping.id == id)

    async def get_all_route_mappings(self) -> Sequence[models.RouteMapping]:
        return await self._select_all()
