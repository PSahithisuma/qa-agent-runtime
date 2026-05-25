from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import (
    HTTPBearer
)

from jose import jwt
from jose import JWTError

from src.auth.security import (
    SECRET_KEY,
    ALGORITHM
)

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):

    token = credentials.credentials

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid token"
        )