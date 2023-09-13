from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status
from slugify import slugify

from src.api.dependencies import get_category_service
from src.database.services import CategoryService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/categories",
    tags=["Categories Endpoint"]
)


@router.post("/create", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_new_category(category: schemas.CategoryCreate, category_service: CategoryService = Depends(get_category_service)):

    category_exists = await category_service.get_category_by_slug(category_slug=slugify(category.name))
    if category_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This category name is already registered.")
    new_category = await category_service.create_category(category)
    return new_category


@router.put("/update", response_model=schemas.CategoryResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def category_update(category: schemas.CategoryUpdate, category_service: CategoryService = Depends(get_category_service)):

    category_db = await category_service.get_category_by_id(id=category.id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {category.id} does not exist")

    updated_category = await category_service.update_category(category)

    return updated_category


@router.delete("/delete/{id}", response_model=schemas.CategoryResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def category_delete(id: int, category_service: CategoryService = Depends(get_category_service)):

    category_db = await category_service.get_category_by_id(id=id)

    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id: {id} does not exist")

    await category_service.delete_category(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("/{category_slug}", response_model=list[schemas.ProductResponse], status_code=status.HTTP_200_OK)
async def fetch_category_products(category_slug: str, offset: int = 0, limit: int = 20, category_service: CategoryService = Depends(get_category_service)):

    category = await category_service.get_category_by_slug(category_slug=category_slug)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category does not exist"
        )

    category_products = await category_service.get_category_products(category_id=category.id, offset=offset, limit=limit)

    if not category_products:
        return []

    return category_products


@router.get("", response_model=Sequence[schemas.CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(category_service: CategoryService = Depends(get_category_service)):

    categories = await category_service.get_all_categories()

    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No category found")

    return categories
