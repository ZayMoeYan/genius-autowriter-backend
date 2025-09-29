from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import database
import enum

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    USER = "User"

class UserStatus(str, enum.Enum):
    ACTIVATE = "Activate"
    DEACTIVATE = "Deactivate"

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVATE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    contents = relationship("Content", back_populates="owner")

class Content(database.Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_posted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="contents")
