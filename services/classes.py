from sqlalchemy.orm import Session
from models import Class
from schemas import ClassCreate
from fastapi import HTTPException
from typing import List, Optional

def get_class(db: Session, class_id: int):
    return db.query(Class).filter(Class.id == class_id).first()



def get_all_classes(db: Session, limit: int = 10, name: str = None):
    query = db.query(Class)
    
    if name:
        query = query.filter(Class.name.ilike(f"%{name}%"))
    
    return query.limit(limit).all()


def create_class(db: Session, class_: ClassCreate):
    # Check for duplicate class name
    existing_class = db.query(Class).filter(Class.name == class_.name).first()
    if existing_class:
        raise HTTPException(status_code=400, detail="Class already exists")

    # Create new class
    db_class = Class(name=class_.name, tagline=class_.tagline)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


# def get_classes_by_name(db: Session, name: str, limit: int = 10):
#     query = db.query(Class)
#     if name:  # If a name is provided, filter the results
#         query = query.filter(Class.name.ilike(f"%{name}%"))  # Case-insensitive search
#     return query.limit(limit).all()