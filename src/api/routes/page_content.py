from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_page_content_service
from src.database.services import PageContentService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/pages",
    tags=["Pages Content Endpoint"]
)


@router.post("/create", response_model=schemas.PageContentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_new_page_content(content: schemas.PageContentCreate, content_service: PageContentService = Depends(get_page_content_service)):

    content_exists = await content_service.get_page_content_by_title(title=content.title)
    if content_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This content is already registered.")
    new_content = await content_service.create_page_content(content)
    return new_content


@router.put("/update", response_model=schemas.PageContentResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def page_content_update(content: schemas.PageContentUpdate, content_service: PageContentService = Depends(get_page_content_service)):

    content_db = await content_service.get_page_content_by_id(id=content.id)

    if not content_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Content with id: {content.id} does not exist")

    updated_content = await content_service.update_page_content(content)

    return updated_content


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def page_content_delete(id: int, content_service: PageContentService = Depends(get_page_content_service)):

    content_db = await content_service.get_page_content_by_id(id=id)

    if not content_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Content with id: {id} does not exist")

    await content_service.delete_page_content(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("", response_model=Sequence[schemas.PageContentResponse], status_code=status.HTTP_200_OK)
async def get_all_page_contents(content_service: PageContentService = Depends(get_page_content_service)):

    contents = await content_service.get_all_page_content()

    if not contents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No page content found")

    return contents
