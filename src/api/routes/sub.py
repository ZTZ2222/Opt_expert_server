from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_sub_service
from src.database.services import SubService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/sub",
    tags=["Subcategories Endpoint"]
)


@router.post("/create", response_model=schemas.SubResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_new_sub(sub: schemas.SubCreate, sub_service: SubService = Depends(get_sub_service)):

    sub_exists = await sub_service.get_sub_by_name(sub_name=sub.name)
    if sub_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This subcategory name is already registered.")
    new_sub = await sub_service.create_sub(sub)
    return new_sub


@router.put("/update", response_model=schemas.SubResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def sub_update(sub: schemas.SubUpdate, sub_service: SubService = Depends(get_sub_service)):

    sub_db = await sub_service.get_sub_by_id(id=sub.id)

    if not sub_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub with id: {sub.id} does not exist")

    updated_sub = await sub_service.update_sub(sub)

    return updated_sub


@router.delete("/delete", response_model=schemas.SubResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def sub_delete(id: int, sub_service: SubService = Depends(get_sub_service)):

    sub_db = await sub_service.get_sub_by_id(id=id)

    if not sub_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sub with id: {id} does not exist")

    deleted_sub = await sub_service.delete_sub(id=id)

    return Response(status_code=status.HTTP_200_OK, content=f"Subcategory with id: {deleted_sub.id} has been deleted")


@router.get("/{id}", response_model=list[schemas.ProductResponse], status_code=status.HTTP_200_OK)
async def fetch_sub_products(id: int, offset: int = 0, limit: int = 20, sub_service: SubService = Depends(get_sub_service)):

    sub_products = await sub_service.get_sub_products(sub_id=id, offset=offset, limit=limit)

    if not sub_products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Products of Sub id: {id} do not exist")

    return sub_products


@router.get("", response_model=Sequence[schemas.SubResponse], status_code=status.HTTP_200_OK)
async def get_all_subs(sub_service: SubService = Depends(get_sub_service)):

    subs = await sub_service.get_all_sub()

    if not subs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No subcategory found")

    return subs
