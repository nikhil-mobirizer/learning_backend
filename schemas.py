from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List



class TopicBase(BaseModel):
    name: str
    details: Optional[str] = None
    
class TopicCreate(TopicBase):
    pass

class TopicData(TopicBase):
    id: int
    name: str
    details: Optional[str] = None

class Topic(TopicBase):
    id: int


    class Config:
        orm_mode = True

class ChapterBase(BaseModel):
    id: int
    name: str

class ChapterCreate(ChapterBase):
    pass

class ChapterData(ChapterBase):
    id: int
    name: str

class Chapter(ChapterBase):
    id: int
    subject_id: int
    topics: list[Topic] = []

    class Config:
        orm_mode = True

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectData(SubjectBase):
    id: int
    name: str

class Subject(SubjectBase):
    id: int
    chapters: list[Chapter] = []

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    name: str

class ClassCreate(ClassBase):
    pass

class ClassData(ClassBase):
    id: int
    subjects: list[Subject] = []

class Class(ClassBase):
    id: int

    class Config:
        orm_mode = True



class GoogleSignInRequest(BaseModel):
    device_id: str
    email: EmailStr
    name: str

class ResponseModel(BaseModel):
    message: str
    data: Optional[Dict] = None


class ChatHistory(BaseModel):
    user: str
    bot: str

class ChatRequest(BaseModel):
    user_query: str

    
class ChatResponse(BaseModel):
    detailed_timeline: Optional[str]
    educational_insights: Optional[str]
