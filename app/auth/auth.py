import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from fastapi.security import OAuth2PasswordBearer


# Load environment variables
load_dotenv()

# Retrieve secrets from environment, raising an error if missing
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Ensure required secrets are set
if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("Missing required environment variables: SECRET_KEY, ALGORITHM, or ACCESS_TOKEN_EXPIRE_MINUTES")

# OAuth2PasswordBearer extracts JWT tokens from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(user_id: int, tenant_id: str) -> str:
    """
    Generate a JWT access token containing `user_id` and `tenant_id`.

    This token will expire in `ACCESS_TOKEN_EXPIRE_MINUTES` minutes.

    Args:
        user_id (int): Unique identifier of the user.
        tenant_id (str): Tenant (schema) identifier.

    Returns:
        str: Encoded JWT access token.
    
    Example:
        ```python
        token = create_access_token(user_id=123, tenant_id="tenant_1")
        ```
    """
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # User ID as subject
        "tenant_id": tenant_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

