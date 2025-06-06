from sqlalchemy import Column, String, Text, Integer, TIMESTAMP, func
from app.utils import Base


class TenantUser(Base):
    __tablename__ = "tenant_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    tenant_schema = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
