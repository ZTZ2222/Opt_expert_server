from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, func, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Content(BaseModel):
    __tablename__ = "content"

    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True, nullable=False)
    slug_en = Column(String)
    image = Column(String, server_default="/Products/placeholder-image.png")

    products = relationship(
        "Product", cascade="all, delete-orphan", lazy="joined", back_populates="category")


class Sub(BaseModel):
    __tablename__ = "sub"

    name = Column(String, unique=True, index=True, nullable=False)
    slug_en = Column(String)

    products = relationship(
        "Product", cascade="all, delete-orphan", lazy="joined", back_populates="sub")


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True, nullable=False)
    article = Column(String, index=True, nullable=False)
    base_price = Column(Numeric(precision=8), nullable=False)
    sale_price = Column(Numeric(precision=8))
    description = Column(Text, nullable=False)
    images = Column(ARRAY(String), default=[
                    "/Products/placeholder-image.png",])
    weight = Column(Numeric(precision=8), nullable=False)
    product_origin = Column(String, nullable=False)
    status = Column(String, default="Активный")
    category_id = Column(Integer, ForeignKey(
        'categories.id', ondelete="CASCADE"), nullable=False)
    sub_id = Column(Integer, ForeignKey(
        'sub.id', ondelete="CASCADE"), nullable=False)
    sizes = Column(ARRAY(String), default=["",])
    slug_en = Column(String)

    category = relationship("Category", back_populates="products")
    sub = relationship("Sub", back_populates="products")
    order_items = relationship(
        'OrderItem', cascade='all, delete-orphan', back_populates='product')


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, server_default="False", nullable=False)
    is_superuser = Column(Boolean, server_default="False", nullable=False)


class Order(BaseModel):
    __tablename__ = "orders"

    full_name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    status = Column(String, nullable=False)

    items = relationship(
        'OrderItem', cascade="all, delete-orphan", backref="order")


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey(
        "orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship(Product, lazy="joined",
                           back_populates='order_items')


class RequestItem(BaseModel):
    __tablename__ = "request_items"

    name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    text = Column(String, nullable=False)


class Size(BaseModel):
    __tablename__ = "sizes"

    name = Column(String, nullable=False)


class PageContent(BaseModel):
    __tablename__ = "page_content"

    title = Column(String, index=True)
    paragraph1 = Column(Text)
    paragraph2 = Column(Text)
    paragraph3 = Column(Text)
    header1 = Column(String)
    body1 = Column(String)
    header2 = Column(String)
    body2 = Column(String)
    header3 = Column(String)
    body3 = Column(String)
    header4 = Column(String)
    body4 = Column(String)
    header5 = Column(String)
    body5 = Column(String)
    header6 = Column(String)
    body6 = Column(String)
    header7 = Column(String)
    body7 = Column(String)
    backgroundImage = Column(String)


class RouteMapping(BaseModel):
    __tablename__ = "route_mapping"

    slug_en = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
