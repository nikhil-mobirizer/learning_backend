from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from database import get_db
import services.topics
from services.auth import get_current_user 

router = APIRouter()

@router.post("/", response_model=schemas.Topic)
def create_topic(
    name: str = Form(...), 
    chapter_id: int = Form(...), 
    details: Optional[str] = Form(None), 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    print(f"Details received: {details}")

    topic = schemas.TopicCreate(name=name, details=details)
    
    db_topic = services.topics.create_topic(db=db, topic=topic, chapter_id=chapter_id)

    if not db_topic:
        raise HTTPException(status_code=400, detail="Chapter not found")
    return db_topic

@router.get("/", response_model=List[schemas.Topic])
def read_all_topics(
    limit: Optional[int] = Form(10),
    name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),   
):
    topics = services.topics.get_all_topics(db, limit=limit, name=name)
    return topics

@router.get("/{topic_id}", response_model=schemas.TopicData)
def read_topic(
    topic_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[str] = Depends(get_current_user), 
):
    db_topic = services.topics.get_topic(db=db, topic_id=topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic

# @router.get("/all_data", response_model=List[schemas.TopicData])
# def read_topics(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     topics = services.topics.get_topics(db, skip=skip, limit=limit)
#     return topics