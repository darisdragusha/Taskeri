import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Dict

# Load environment variables
load_dotenv()

class AuthService:
    """Handles authentication logic, including token generation and verification."""

    def __init__(self):
        """Initialize AuthService with environment-configured settings."""
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

        # Ensure all required environment variables are set
        if not self.SECRET_KEY or not self.ALGORITHM or not self.ACCESS_TOKEN_EXPIRE_MINUTES:
            raise ValueError("Missing required environment variables: SECRET_KEY, ALGORITHM, or ACCESS_TOKEN_EXPIRE_MINUTES")

        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_access_token(self, user_id: int, tenant_id: str) -> str:
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
            token = auth_service.create_access_token(user_id=123, tenant_id="tenant_1")
            ```
        """
        expire = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),  # User ID as subject
            "tenant_id": tenant_id,
            "exp": expire
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, token: str) -> Dict:
        """
        Decode and validate a JWT token.

        If the token is valid, extracts `user_id` and `tenant_id`. 
        Otherwise, raises an HTTP 401 Unauthorized error.

        Args:
            token (str): The JWT token.

        Returns:
            dict: Decoded token payload containing:
                - `user_id` (int)
                - `tenant_id` (str)

        Raises:
            HTTPException: If the token is invalid or expired.
        
        Example:
            ```python
            payload = auth_service.verify_token(token)
            print(payload["user_id"], payload["tenant_id"])
            ```
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = payload.get("sub")
            tenant_id = payload.get("tenant_id")

            if not user_id or not tenant_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return {"user_id": int(user_id), "tenant_id": tenant_id}

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> Dict:
        """
        Extract `user_id` and `tenant_id` from a valid JWT token.

        This function acts as a FastAPI dependency for protected routes.

        Args:
            token (str): The JWT token obtained from the request.

        Returns:
            dict: Dictionary with:
                - `user_id` (int)
                - `tenant_id` (str)

        Raises:
            HTTPException: If the token is invalid or expired.
        
        Example:
            ```python
            user = auth_service.get_current_user(token)
            print(user["user_id"], user["tenant_id"])
            ```
        """
        return self.verify_token(token)


# Instantiate a global authentication service instance
auth_service = AuthService()