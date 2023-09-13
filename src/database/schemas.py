from datetime import datetime
from enum import Enum
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
    slug_en: Optional[str]
    image: str


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


###########
# Product #
###########


class ProductCreate(BaseModel):
    id: Optional[int]
    name: str
    article: str
    base_price: int
    sale_price: Optional[int]
    description: str
    images: Optional[list[str]]
    status: str = "Активный"
    weight: int
    product_origin: str
    category_id: int
    sub_id: int
    sizes: list[str]
    slug_en: Optional[str]


class ProductUpdate(ProductCreate):
    created_at: datetime | str = None
    updated_at: datetime | str = None

    class Config:
        orm_mode = True


class ProductResponse(ProductUpdate):
    category: Optional[CategoryResponse]
    sub: Optional[SubResponse]

    class Config:
        orm_mode = True


##############
# Order Item #
##############


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemUpdate(OrderItemCreate):
    order_id: int


class OrderItemResponse(OrderItemUpdate):
    product: ProductUpdate
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


#########
# Order #
#########


class OrderStatus(str, Enum):
    Оформлен = "Оформлен"
    Оплачен = "Оплачен"
    В_пути = "В пути"
    Доставлен = "Доставлен"
    Возврат = "Возврат"


class OrderCreate(BaseModel):
    full_name: str
    telephone: str
    status: OrderStatus = "Оформлен"
    items: list[OrderItemCreate]


class OrderUpdate(OrderCreate):
    id: int
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
    password: str
    is_staff: Optional[bool]
    is_superuser: Optional[bool]


class UserUpdate(UserCreate):
    id: Optional[int]
    password: Optional[str]


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


###########
# Request #
###########

class RequestItemCreate(BaseModel):
    name: str
    telephone: str
    text: str


class RequestItem(RequestItemCreate):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


########
# Size #
########

class SizeCreate(BaseModel):
    name: str


class Size(SizeCreate):
    id: int

    class Config:
        orm_mode = True


################
# Page Content #
################


class PageContentCreate(BaseModel):
    title: Optional[str]
    paragraph1: Optional[str]
    paragraph2: Optional[str]
    paragraph3: Optional[str]
    header1: Optional[str]
    body1: Optional[str]
    header2: Optional[str]
    body2: Optional[str]
    header3: Optional[str]
    body3: Optional[str]
    header4: Optional[str]
    body4: Optional[str]
    header5: Optional[str]
    body5: Optional[str]
    header6: Optional[str]
    body6: Optional[str]
    header7: Optional[str]
    body7: Optional[str]
    backgroundImage: Optional[str]


class PageContentUpdate(PageContentCreate):
    id: int


class PageContentResponse(PageContentUpdate):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


################
# Slug Mapping #
################

class RouteMapping(BaseModel):
    id: Optional[int]
    slug_en: str
    name: str

    class Config:
        orm_mode = True
