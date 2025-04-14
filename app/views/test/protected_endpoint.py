from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from auth.auth import auth_service  # This is where `get_current_user` would be defined
from utils.db_utils import get_db  # Your DB connection file containing the `get_db` dependency

router = APIRouter()

@router.get("/protected")
def protected_route(
    db: Session = Depends(get_db),  # Database session
    current_user: dict = Depends(auth_service.get_current_user)):
    """
    A protected route that requires authentication.

    Args:
        user (dict): Extracted user details from the token.

    Returns:
        dict: User ID and Tenant ID.
    """
    return {
        "message": "You have accessed a protected route!",
        "user_id": current_user["user_id"],
        "tenant_id": current_user["tenant_id"]
    }
