from fastapi import APIRouter

from .routes import login, employees, tips

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(employees.router, prefix="/employee", tags=["users"])
api_router.include_router(tips.router, prefix="/tips", tags=["tips"])