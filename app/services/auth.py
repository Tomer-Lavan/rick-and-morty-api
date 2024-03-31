# app/services/auth.py

import jwt
from datetime import datetime, timedelta
from typing import Optional

# In production needs to move to an env file and update SECRET_KEY.
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JSON Web Token (JWT) for authentication.
    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta], optional): The expiration time delta for the token. Defaults to None.
    Returns:
        str: The encoded JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verifies a JSON Web Token (JWT) and returns its payload.
    Args:
        token (str): The JWT to verify.
    Returns:
        Optional[dict]: The payload of the token if verification is successful, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
