from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..dependencies import get_user_service, admin_only
from src.database import schemas
from src.database.services import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users Endpoint"]
)


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_only)])
async def create_new_user(user_credentials: schemas.UserCreate, user_service: UserService = Depends(get_user_service)):

    user_exists = await user_service.get_user_by_email(email=user_credentials.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email address is already registered.")
    new_user = await user_service.create_user(user_credentials)
    return new_user


@router.put("/update", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def user_update(user_credentials: schemas.UserUpdate, user_service: UserService = Depends(get_user_service)):

    user = await user_service.get_user_by_email(email=user_credentials.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user_credentials.email} does not exist")

    updated_user = await user_service.update_user(user_credentials)

    return updated_user


@router.delete("/delete", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def user_delete(user_credentials: schemas.UserUpdate, user_service: UserService = Depends(get_user_service)):

    user = await user_service.get_user_by_id(id=user_credentials.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_credentials.id} does not exist")

    deleted_user = await user_service.delete_user(user_credentials)

    return Response(status_code=status.HTTP_200_OK, content=f"User with id: {deleted_user.id} has been deleted")


@router.get("/", response_model=Sequence[schemas.UserResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def users_get_all(user_service: UserService = Depends(get_user_service)):

    users = await user_service.get_all_users()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users found")

    return users
