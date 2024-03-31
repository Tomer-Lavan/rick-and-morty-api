from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import mock_users_db
from app.services.auth import create_access_token
from datetime import timedelta

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user based on username and password.
    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
    Returns:
        dict: Access token and token type if authentication is successful.
    Raises:
        HTTPException: If username or password is incorrect.
    """

    # Currently Retrieve the user from a mock database
    user = mock_users_db.get(form_data.username)
    if not user or user.get("password") != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=240)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
