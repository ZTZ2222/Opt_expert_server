from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_request_item_service
from src.database.services import RequestItemService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/request",
    tags=["Product Requests Endpoint"]
)


@router.post("/create", response_model=schemas.RequestItem, status_code=status.HTTP_201_CREATED)
async def create_new_request_item(request_item: schemas.RequestItemCreate, request_item_service: RequestItemService = Depends(get_request_item_service)):
    return await request_item_service.create_request_item(request_item)


@router.delete("/delete/{id}", response_model=schemas.RequestItem, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def request_item_delete(id: int, request_item_service: RequestItemService = Depends(get_request_item_service)):

    request_item_db = await request_item_service.get_request_item_by_id(id=id)

    if not request_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Request with id: {id} does not exist")

    await request_item_service.delete_request_item(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("", response_model=Sequence[schemas.RequestItem], status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def get_all_request_items(request_item_service: RequestItemService = Depends(get_request_item_service)):

    request_items = await request_item_service.get_all_request_items()

    if not request_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No request items found")

    return request_items
