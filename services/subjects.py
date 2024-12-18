from sqlalchemy.orm import Session
from models import Subject
from schemas import SubjectCreate


def get_subjects_by_class(db: Session, class_id: int):
    return db.query(Subject).filter(Subject.class_id == class_id).all()

# Get all subjects from the database
def get_all_subjects(db: Session, limit: int = 10, name: str = None):
    query = db.query(Subject)
    print("----hi---", name)
    if name:
        query = query.filter(Subject.name.ilike(f"%{name}%"))
    return query.limit(limit).all()

# Create a new subject in the database
def create_subject(db: Session, subject: SubjectCreate, class_id: int):
    db_subject = Subject(name=subject.name, class_id=class_id)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject
