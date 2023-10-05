import base64
import os
import uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import schemas
from .database.database import db
from .database import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def create_access_token(token_payload: dict[str:Any]) -> str:
    to_encode = token_payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(token: str, credential_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None:
            raise credential_exception

        token_data = schemas.TokenPayload(user_id=user_id, email=email)

    except JWTError:
        raise credential_exception

    return token_data


async def get_current_user(token: str = Depends(reusable_oauth2), session: AsyncSession = Depends(db.get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_verified = await verify_access_token(token, credentials_exception)
    async with session:
        user = await session.scalar(select(models.User).filter(models.User.email == token_verified.email))
    return user


def upload_product_images(images: list[str]) -> list[str]:
    image_urls = []

    for image_data in images:
        # Extract the file extension from the base64 image data
        file_extension = '.' + image_data.split('/')[1].split(';')[0]

       # Generate a unique filename using UUID
        unique_id = str(uuid.uuid4())
        dynamic_filename = f"productImage_{unique_id}{file_extension}"

        # Decode the base64 image data
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # Specify the directory where you want to save the image
        directory = f"{os.getenv('MEDIA_URL')}/ProductImages"

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Specify the save path for the image
        save_path = os.path.join(directory, dynamic_filename)

        # Save the image to the specified path
        with open(save_path, 'wb') as f:
            f.write(image_bytes)

        # Store the generated image filename
        image_urls.append(
            f"{os.getenv('MEDIA_URL')}/ProductImages/{dynamic_filename}")

    return image_urls


def upload_category_image(image_base64: str) -> str:
    # Extract the file extension from the base64 image data
    file_extension = '.' + image_base64.split('/')[1].split(';')[0]

    # Generate a unique filename using UUID
    unique_id = str(uuid.uuid4())
    dynamic_filename = f"categoryImage_{unique_id}{file_extension}"

    # Decode the base64 image data
    image_base64 = image_base64.split(',')[1]
    image = base64.b64decode(image_base64)

    # Specify the directory where you want to save the image
    directory = f"{os.getenv('MEDIA_URL')}/CategoryImages"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Specify the save path for the image
    save_path = os.path.join(directory, dynamic_filename)

    # Save the image to the specified path
    with open(save_path, 'wb') as f:
        f.write(image)

    # Store the generated image filename
    image_url = f"{os.getenv('MEDIA_URL')}/CategoryImages/{dynamic_filename}"

    return image_url


def upload_content_image(image_base64: str) -> str:
    # Extract the file extension from the base64 image data
    file_extension = '.' + image_base64.split('/')[1].split(';')[0]

    # Generate a unique filename using UUID
    unique_id = str(uuid.uuid4())
    dynamic_filename = f"contentImage_{unique_id}{file_extension}"

    # Decode the base64 image data
    image_base64 = image_base64.split(',')[1]
    image = base64.b64decode(image_base64)

    # Specify the directory where you want to save the image
    directory = f"{os.getenv('MEDIA_URL')}/ContentImages"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Specify the save path for the image
    save_path = os.path.join(directory, dynamic_filename)

    # Save the image to the specified path
    with open(save_path, 'wb') as f:
        f.write(image)

    # Store the generated image filename
    image_url = f"{os.getenv('MEDIA_URL')}/ContentImages/{dynamic_filename}"

    return image_url
