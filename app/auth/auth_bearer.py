from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# =========================================================
# BEARER AUTHENTICATION
# =========================================================

bearer_scheme = HTTPBearer()


# =========================================================
# VERIFY JWT TOKEN
# =========================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):
    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token."
            )

        return {
            "user_id": user_id,
            "role": payload.get("role")
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )