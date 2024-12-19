from sqlalchemy.orm import Session
from models import Chapter
from schemas import ChapterCreate
from sqlalchemy.orm import joinedload

# CRUD operations for Chapter
def get_chapter(db: Session, chapter_id: int):
    return db.query(Chapter).filter(Chapter.id == chapter_id).first()

def get_all_chapters(db: Session, limit: int = 10, name: str = None):
    query = db.query(Chapter)
    
    if name:
        query = query.filter(Chapter.name.ilike(f"%{name}%"))
    
    return query.limit(limit).all()


def create_chapter(db: Session, chapter: ChapterCreate, subject_id: int):
    db_chapter = Chapter(name=chapter.name, subject_id=subject_id, tagline=chapter.tagline)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def get_chapters_by_subject(db: Session, subject_id: int):
    return db.query(Chapter).filter(Chapter.subject_id == subject_id).all()
    

# def get_chapters(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Chapter).options(joinedload(Chapter.topics)).offset(skip).limit(limit).all()


