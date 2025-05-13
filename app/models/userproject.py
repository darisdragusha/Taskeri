from sqlalchemy import Column, BigInteger, ForeignKey, UniqueConstraint
from utils.db_utils import Base

class UserProject(Base):
    __tablename__ = "user_projects"
    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', name='uq_user_project'),
        {"schema": None},
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    project_id = Column(BigInteger, ForeignKey("projects.id"), primary_key=True)
