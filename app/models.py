from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  title = Column(String(50), nullable=False)
  content = Column(String(255), nullable=False)
  published = Column(Boolean, server_default="1")
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

  # mapping a foreign key constraint
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

  # sqlalchemy relationships
  owner = relationship("User")

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  email = Column(String(100), nullable=False, unique=True)
  password = Column(String(100), nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)