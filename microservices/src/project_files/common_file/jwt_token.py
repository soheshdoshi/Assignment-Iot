import os
import logging
import sys
import traceback

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


def create_access_token(data: dict):
    """
    this method will create basic jwt token.
    """
    logging.info("[INFO] :: creating access token")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=3000)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def auth_validation(auth_headers):
    """
    this method will handle all auth validation part.
    """
    scheme, token = auth_headers.split()
    if scheme.lower() != "bearer":
        logging.info("[INFO] :: bearer not found in headers schema.")
        return {"error": 401}
    try:
        if SECRET_KEY is None or not isinstance(SECRET_KEY, str):
            return {"error": 401}

        # payload decode part
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("username")
        if username is None:
            logging.info("[INFO] :: Invalid Payload.")
            return {"error": 401}

    except JWTError:
        traceback.print_exc(*sys.exc_info())
        return {"error": 401}

    return payload
