import logging
import os
import traceback


from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.security import create_access_token
from src.logger import logging_middleware
from src.address_book.router import router as address_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)


@app.get("/", tags=["Root"])
async def status_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/token",
    tags=["Auth"],
    description="Retrieve a JWT access token easily for demonstration purposes.",
)
async def get_access_token() -> str:
    """
    Endpoint to retrieve a JWT access token.
    Only for demonstration purposes.
    """
    return create_access_token()


app.include_router(address_router, prefix="/addr", tags=["Address Book"])
