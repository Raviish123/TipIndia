from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from routing.app import api_router
from utils.db import init_db

app = FastAPI()


# TODO: Set up a config.py with Pydantic BaseSettings for origins, domain, etc. to link to .env
origins = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost',
    'https://localhost:3000',
    'https://localhost:5173',
    'https://localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        str(origin).strip("/") for origin in origins
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

init_db()

app.include_router(api_router, prefix="/api")