from fastapi import APIRouter

from .routes import user, category, auth, order, product, sub, request_item, size, content, page_content


api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(category.router)
api_router.include_router(auth.router)
api_router.include_router(order.router)
api_router.include_router(product.router)
api_router.include_router(sub.router)
api_router.include_router(request_item.router)
api_router.include_router(size.router)
api_router.include_router(content.router)
api_router.include_router(page_content.router)
