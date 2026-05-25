from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from src.auth.security import (
    create_access_token
)

router = APIRouter()


class LoginRequest(BaseModel):

    username: str

    password: str


@router.post("/login")
async def login(
    request: LoginRequest
):

    # DEMO USERS
    # Replace later with database lookup

    demo_users = {

        "admin": {
            "password": "admin123",
            "role": "admin"
        },

        "developer": {
            "password": "dev123",
            "role": "developer"
        },

        "viewer": {
            "password": "view123",
            "role": "viewer"
        }
    }

    user = demo_users.get(
        request.username
    )

    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid username"
        )

    if user["password"] != request.password:

        raise HTTPException(

            status_code=401,

            detail="Invalid password"
        )

    access_token = create_access_token({

        "sub": request.username,

        "role": user["role"]
    })

    return {

        "access_token": access_token,

        "token_type": "bearer",

        "role": user["role"]
    }