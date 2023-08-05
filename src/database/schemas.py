from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

###########
# Content #
###########


class ContentCreate(BaseModel):
    title: str
    description: str


class ContentUpdate(ContentCreate):
    id: int


class ContentResponse(ContentUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


############
# Category #
############


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(CategoryCreate):
    id: int


class CategoryResponse(CategoryUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


#######
# Sub #
#######


class SubCreate(BaseModel):
    name: str


class SubUpdate(SubCreate):
    id: int


class SubResponse(SubUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


#############
# Inventory #
#############


class InventoryDTO(BaseModel):
    id: Optional[int]
    product_id: Optional[int]
    size: str
    quantity: int


class InventoryResponse(BaseModel):
    size: str
    quantity: int

    class Config:
        orm_mode = True


###########
# Product #
###########


class ProductCreate(BaseModel):
    name: str = "Unnamed product"
    article: str
    base_price: int
    sale_price: Optional[int]
    description: Optional[str]
    weight: Optional[int]
    product_origin: Optional[str]
    category_id: int
    sub_id: int
    inventory: list[InventoryDTO]


class ProductUpdate(ProductCreate):
    id: int


class ProductDelete(BaseModel):
    id: int


class ProductResponse(ProductUpdate):
    inventory: list[InventoryResponse]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


##############
# Order Item #
##############


class OrderItemCreate(BaseModel):
    product_id: int
    size: str
    quantity: int
    price: float


class OrderItemUpdate(OrderItemCreate):
    order_id: int


class OrderItemResponse(OrderItemUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


#########
# Order #
#########


class OrderCreate(BaseModel):
    full_name: str
    telephone: str
    items: list[OrderItemCreate]


class OrderUpdate(OrderCreate):
    id: int
    paid: Optional[bool]
    delivered: Optional[bool]
    returned: Optional[bool]
    items: list[OrderItemUpdate]


class OrderResponse(OrderUpdate):
    items: list[OrderItemResponse]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


########
# User #
########


class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str]
    is_staff: Optional[bool]
    is_superuser: Optional[bool]


class UserUpdate(UserCreate):
    id: Optional[int]


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


#########
# Token #
#########


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    exp: Optional[int] = None
