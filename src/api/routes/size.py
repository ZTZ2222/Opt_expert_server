from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_size_service
from src.database.services import SizeService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/size",
    tags=["Product Sizes Endpoint"]
)


@router.post("/create", response_model=schemas.Size, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_new_size(size: schemas.SizeCreate, size_service: SizeService = Depends(get_size_service)):
    return await size_service.create_size(size)


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def size_delete(id: int, size_service: SizeService = Depends(get_size_service)):

    size_db = await size_service.get_size_by_id(id=id)

    if not size_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Size with id: {id} does not exist")

    deleted_size = await size_service.delete_size(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("", response_model=Sequence[schemas.Size], status_code=status.HTTP_200_OK)
async def get_all_sizes(size_service: SizeService = Depends(get_size_service)):

    sizes = await size_service.get_all_sizes()

    if not sizes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No request items found")

    return sizes
