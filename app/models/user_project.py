from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint
from app.utils.db_utils import Base

class UserProject(Base):
    __tablename__ = "user_projects"
    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', name='uq_user_project'),
        {"schema": None},
    )

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
