from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import get_product_service
from src.database.services import ProductService
from src.database import schemas
from src.api.dependencies import staff_only

router = APIRouter(
    prefix="/products",
    tags=["Products Endpoint"]
)


@router.post("/create", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_product(product: schemas.ProductCreate, product_service: ProductService = Depends(get_product_service)):
    try:
        result = await product_service.create_product(product)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.put("/update", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def update_product(product: schemas.ProductUpdate, product_service: ProductService = Depends(get_product_service)):
    try:
        result = await product_service.update_product(product)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def delete_product(product: schemas.ProductUpdate, product_service: ProductService = Depends(get_product_service)):

    deleted_product = await product_service.delete_product(product.id)
    if not deleted_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product has been not found")
    return {"detail": f"Product with id: {deleted_product.id} has been successfully deleted"}


@router.get("/{id}", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(id: int, product_service: ProductService = Depends(get_product_service)):

    result = await product_service.get_product_by_id(id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with key id: {id} does not exists"
        )
    return result


@router.get("", response_model=Sequence[schemas.ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(offset: int = 0, limit: int = 20, product_service: ProductService = Depends(get_product_service)):

    result = await product_service.get_all_products(offset=offset, limit=limit)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products do not exist"
        )
    return result
