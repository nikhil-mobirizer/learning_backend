from sqlalchemy.orm import Session
from models import Topic
from schemas import TopicCreate


# CRUD operations for Topic
def get_topic(db: Session, topic_id: int):
    return db.query(Topic).filter(Topic.id == topic_id).first()

# def get_topics(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Topic).offset(skip).limit(limit).all()

def get_all_topics(db: Session, limit: int = 10, name: str = None):
    query = db.query(Topic)
    
    if name:
        query = query.filter(Topic.name.ilike(f"%{name}%"))
    
    return query.limit(limit).all()


def create_topic(db: Session, topic: TopicCreate, chapter_id: int):
    db_topic = Topic(name=topic.name,  details=topic.details, chapter_id=chapter_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic