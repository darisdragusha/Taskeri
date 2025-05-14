import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Dict
from functools import lru_cache
from utils.env_utils import EnvironmentVariable, get_env

class AuthService:
    """
    Handles authentication logic, including token generation and verification.
    
    This service provides methods for creating JWT access tokens, verifying them,
    and extracting user details from the token.
    """

    # Load environment variables from env_utils
    SECRET_KEY: str = get_env(EnvironmentVariable.SECRET_KEY, "")
    ALGORITHM: str = get_env(EnvironmentVariable.ALGORITHM, "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_env(EnvironmentVariable.ACCESS_TOKEN_EXPIRE_MINUTES, "30"))

    if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
        raise ValueError("Missing required environment variables: SECRET_KEY, ALGORITHM, or ACCESS_TOKEN_EXPIRE_MINUTES")

    ALGORITHM_SET: set[str] = {ALGORITHM}  # Preload as a set for faster lookup

    @lru_cache()
    def get_oauth2_scheme() -> OAuth2PasswordBearer:
        """Cache the OAuth2PasswordBearer instance to reduce memory overhead."""
        return OAuth2PasswordBearer(tokenUrl="token")

    oauth2_scheme: OAuth2PasswordBearer = get_oauth2_scheme()

    def create_access_token(self, user_id: int, tenant_id: int, tenant_name: str) -> str:
        """
        Generate a JWT access token containing `user_id`, `tenant_id`, and `tenant_name`.

        This token will expire in `ACCESS_TOKEN_EXPIRE_MINUTES` minutes.

        Args:
            user_id (int): Unique identifier of the user.
            tenant_id (int): Tenant (schema) identifier.
            tenant_name (str): Name of the tenant.

        Returns:
            str: Encoded JWT access token.
        """
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload: Dict[str, str | int | datetime] = {
            "sub": str(user_id),
            "tenant_id": tenant_id,
            "tenant_name": tenant_name,
            "exp": expire
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, token: str) -> Dict[str, int | str]:
        """
        Decode and validate a JWT token.

        If the token is valid, extracts `user_id`, `tenant_id`, and `tenant_name`. 
        Otherwise, raises an HTTP 401 Unauthorized error.

        Args:
            token (str): The JWT token.

        Returns:
            dict: Decoded token payload containing:
                - `user_id` (int)
                - `tenant_id` (int)
                - `tenant_name` (str)

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            payload: Dict[str, str] = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM_SET)
            user_id = payload.get("sub")
            tenant_id = payload.get("tenant_id")
            tenant_name = payload.get("tenant_name")
            exp = payload.get("exp")

            if not all([user_id, tenant_id, tenant_name, exp]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Explicit expiration check
            if datetime.now(timezone.utc).timestamp() > float(exp):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return {
                "user_id": int(user_id),
                "tenant_id": int(tenant_id),
                "tenant_name": tenant_name
            }

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_user(self, token: str = Depends(oauth2_scheme)) -> Dict[str, int | str]:
        """
        Extract `user_id`, `tenant_id`, and `tenant_name` from a valid JWT token.

        This function acts as a FastAPI dependency for protected routes.

        Args:
            token (str): The JWT token obtained from the request.

        Returns:
            dict: Dictionary with:
                - `user_id` (int)
                - `tenant_id` (int)
                - `tenant_name` (str)

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        return self.verify_token(token)
    
auth_service: AuthService = AuthService()