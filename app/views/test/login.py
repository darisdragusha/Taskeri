from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import auth_service

router = APIRouter()

# Mock user credentials
MOCK_USER = {
    "username": "testuser",
    "password": "password123",
    "user_id": 1,
    "tenant_id": "tenant_1"
}

@router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The user's login credentials.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: If credentials are invalid.
    """
    if form_data.username == MOCK_USER["username"] and form_data.password == MOCK_USER["password"]:
        token = auth_service.create_access_token(
            user_id=MOCK_USER["user_id"],
            tenant_id=MOCK_USER["tenant_id"]
        )
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
