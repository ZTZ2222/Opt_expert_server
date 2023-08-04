from fastapi import APIRouter

from .routes import user, category, auth, order, product


api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(category.router)
api_router.include_router(auth.router)
api_router.include_router(order.router)
api_router.include_router(product.router)
