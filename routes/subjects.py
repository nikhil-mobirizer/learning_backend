from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
import services.subjects
from services.auth import get_current_user 
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=schemas.Subject)
def create_subject(
    name: str = Form(...),
    tagline: Optional[str] = Form(None),
    class_id: int = Form(...), 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    subject = schemas.SubjectCreate(name=name, tagline=tagline)
    
    db_subject = services.subjects.create_subject(db=db, subject=subject, class_id=class_id)

    if not db_subject:
        raise HTTPException(status_code=400, detail="Class not found")
    return db_subject

@router.get("/", response_model=List[schemas.SubjectData])
def read_all_subjects(
    limit: Optional[int] = Form(10),
    name: Optional[str] = Form(None), 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    subjects = services.subjects.get_all_subjects(db, limit=limit, name=name)
    return subjects

@router.get("/class/{class_id}", response_model=List[schemas.SubjectData])
async def get_subjects_by_class(
    class_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    subjects = services.subjects.get_subjects_by_class(db, class_id)
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found for the class")
    return subjects

















# @router.get("/all_data", response_model=List[schemas.SubjectData])
# def read_subjects(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     subjects = services.subjects.get_subjects(db, skip=skip, limit=limit)
#     return subjects

# @router.get("/{subject_id}", response_model=schemas.Subject)
# def read_subject(subject_id: int, db: Session = Depends(get_db)):
#     db_subject = services.subjects.get_subject(db=db, subject_id=subject_id)
#     if db_subject is None:
#         raise HTTPException(status_code=404, detail="Subject not found")
#     return db_subject