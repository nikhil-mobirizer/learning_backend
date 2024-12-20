from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tagline = Column(String, nullable=True)
    subjects = relationship("Subject", back_populates="class_")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    tagline = Column(String, nullable=True)
    class_ = relationship("Class", back_populates="subjects")
    chapters = relationship("Chapter", back_populates="subject")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    tagline = Column(String, nullable=True)
    subject = relationship("Subject", back_populates="chapters")
    topics = relationship("Topic", back_populates="chapter")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    details = Column(String, nullable=True)
    tagline = Column(String, nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    chapter = relationship("Chapter", back_populates="topics")

# User model
class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True,default=lambda: str(uuid.uuid4()), index=True)
    device_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    mobile_number = Column(String, unique=True, index=True, nullable=False)
    otp = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    email = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    occupation = Column(String, nullable=True)
    image_link = Column(String, nullable=True)


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    user_id = Column(String, index=True) 
    user = Column(String, index=True)
    bot = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow) 
