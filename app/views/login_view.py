from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from controllers import LoginController
from utils.db_utils import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return a JWT token.

    The login endpoint takes an email and password (from form data),
    verifies the credentials, and if successful, generates a JWT token
    for the user. This token can then be used for subsequent authenticated requests.
    """
    login_controller = LoginController(db)

    # Authenticate user and generate the access token
    access_token = await login_controller.authenticate_user(form_data.username, form_data.password)

    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": access_token, "token_type": "bearer"}
