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
        orm_mode = True


########
# User #
########
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_staff: bool


class UserUpdate(UserCreate):
    id: int


class UserResponse(UserUpdate):
    is_superuser: bool
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class UserPrivileges(BaseModel):
    email: EmailStr
    is_superuser: bool
