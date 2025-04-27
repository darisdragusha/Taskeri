from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from controllers.login_controller import LoginController
from utils.db_utils import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    """
    Request body schema for login endpoint.
    This model expects the user's `email` and `password`.
    """
    email: str
    password: str

@router.post("/token", response_model=dict)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return a JWT token.

    The login endpoint takes a email and password, verifies the credentials,
    and if successful, generates a JWT token for the user. This token can then
    be used for subsequent authenticated requests.

    """
    # Initialize the controller with the database session
    login_controller = LoginController(db)

    # Authenticate user and generate the access token
    access_token = await login_controller.authenticate_user(request.email, request.password)

    # If authentication fails, raise an HTTPException
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}