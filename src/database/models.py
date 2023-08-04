from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, func
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

    title = Column(String, index=True)
    description = Column(Text, nullable=False)


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, unique=True, index=True)

    products = relationship(
        "Product", cascade="all, delete-orphan", lazy="joined")


class Sub(BaseModel):
    __tablename__ = "sub"

    name = Column(String, unique=True, index=True)

    products = relationship(
        "Product", cascade="all, delete-orphan", lazy="joined")


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True)
    article = Column(String, index=True)
    base_price = Column(Numeric(precision=8), server_default="1")
    sale_price = Column(Numeric(precision=8), nullable=True)
    description = Column(Text, nullable=True)
    weight = Column(Numeric(precision=8), nullable=True)
    product_origin = Column(String)
    category_id = Column(Integer, ForeignKey(
        'categories.id', ondelete="CASCADE"), nullable=False)
    sub_id = Column(Integer, ForeignKey(
        'sub.id', ondelete="CASCADE"), nullable=False)

    inventory = relationship("Inventory")


class Inventory(BaseModel):
    __tablename__ = "inventory"

    product_id = Column(Integer, ForeignKey("products.id"))
    size = Column(String)
    quantity = Column(Integer)


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, server_default="False")
    is_superuser = Column(Boolean, server_default="False")


class Order(BaseModel):
    __tablename__ = "orders"

    full_name = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    paid = Column(Boolean, default=False)
    delivered = Column(Boolean, default=False)
    returned = Column(Boolean, default=False)

    items = relationship('OrderItem', back_populates="order")


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
