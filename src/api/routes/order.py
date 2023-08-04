from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import get_order_service
from src.database.services import OrderService
from src.database import schemas
from src.api.dependencies import staff_only

router = APIRouter(
    prefix="/orders",
    tags=["Orders Endpoint"]
)


@router.post("/create", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate, order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.create_order(order)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.put("/return", response_model=schemas.OrderResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def return_order(order: schemas.OrderUpdate, order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.return_order(order)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.put("/update", response_model=schemas.OrderResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def update_order_info(order: schemas.OrderUpdate, order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.update_order_info(order)

    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error.orig).split("\n")[-1].replace("DETAIL:  ", "")
        )
    return result


@router.get("/", response_model=Sequence[schemas.OrderResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def get_all_orders(offset: int = 0, limit: int = 20, order_service: OrderService = Depends(get_order_service)):

    orders = await order_service.get_all_orders(offset=offset, limit=limit)

    if not orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Orders do not exist.")

    return orders


@router.get("/{order_id}", response_model=schemas.OrderResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def get_order(order_id: int, order_service: OrderService = Depends(get_order_service)):

    order = await order_service.get_order_by_id(id=order_id)

    if not order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Order id: {order_id} doesn't exist.")

    return order
