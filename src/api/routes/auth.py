from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.schemas import Token
from src.database.database import db
from src.database import models
from src.utils import pwd_context, create_access_token


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db.get_session)):
    async with session:
        user = await session.scalar(select(models.User).filter(models.User.email == user_credentials.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    if not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    access_token = await create_access_token(
        token_payload={
            "user_id": user.id,
            "email": user.email,
        }
    )

    return {"token_type": "Bearer", "access_token": access_token}
