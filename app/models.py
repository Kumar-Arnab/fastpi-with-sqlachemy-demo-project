from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  title = Column(String(50), nullable=False)
  content = Column(String(255), nullable=False)
  published = Column(Boolean, server_default="1")
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)