from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_content_service, get_route_mapping_service
from src.database.services import ContentService, RouteMappingService
from src.database import schemas
from src.api.dependencies import staff_only


router = APIRouter(
    prefix="/content",
    tags=["Content Endpoint"]
)


@router.post("/create", response_model=schemas.ContentResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(staff_only)])
async def create_new_content(content: schemas.ContentCreate, content_service: ContentService = Depends(get_content_service)):

    content_exists = await content_service.get_content_by_title(title=content.title)
    if content_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This content is already registered.")
    new_content = await content_service.create_content(content)
    return new_content


@router.put("/update", response_model=schemas.ContentResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def content_update(content: schemas.ContentUpdate, content_service: ContentService = Depends(get_content_service)):

    content_db = await content_service.get_content_by_id(id=content.id)

    if not content_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Content with id: {content.id} does not exist")

    updated_content = await content_service.update_content(content)

    return updated_content


@router.delete("/delete/{id}", response_model=schemas.ContentResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def content_delete(id: int, content_service: ContentService = Depends(get_content_service)):

    content_db = await content_service.get_content_by_id(id=id)

    if not content_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Content with id: {id} does not exist")

    await content_service.delete_content(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.get("", response_model=Sequence[schemas.ContentResponse], status_code=status.HTTP_200_OK)
async def get_all_contents(content_service: ContentService = Depends(get_content_service)):

    contents = await content_service.get_all_content()

    if not contents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No content found")

    return contents


@router.get("/route-mapping", response_model=Sequence[schemas.RouteMapping], status_code=status.HTTP_200_OK)
async def get_all_route_mappings(route_mapping_service: RouteMappingService = Depends(get_route_mapping_service)):

    route_mappings = await route_mapping_service.get_all_route_mappings()

    if not route_mappings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No content found")

    return route_mappings
