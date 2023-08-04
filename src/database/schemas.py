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
        from_attributes = True


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
        from_attributes = True


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
        from_attributes = True


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
        from_attributes = True


###########
# Product #
###########


class ProductCreate(BaseModel):
    name: str = "Unnamed product"
    article: str
    base_price: int
    sale_price: Optional[int]
    description: Optional[str]
    weight: Optional[str]
    product_origin: Optional[str]
    category_id: int
    sub_id: int
    inventory: InventoryDTO


class ProductUpdate(ProductCreate):
    id: int
    category_id: Optional[int]
    inventory: Optional[InventoryDTO]


class ProductResponse(ProductUpdate):
    inventory: list[InventoryResponse]
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


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
        from_attributes = True


##############
# Order Item #
##############


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
        from_attributes = True


########
# User #
########


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_staff: bool
    is_superuser: Optional[bool]


class UserUpdate(UserCreate):
    id: int


class UserResponse(UserUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


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
