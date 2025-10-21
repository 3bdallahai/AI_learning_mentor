from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.db.database import base

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", back_populates="users")

class Chat(base):
    __tablename__ = "chats"

    id= Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question= Column(Text)
    answer= Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user= relationship("User", back_populates="chats")
