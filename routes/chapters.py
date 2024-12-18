from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List, Optional
import schemas
from database import get_db
import services.chapters
from sqlalchemy.orm import Session
from services.auth import get_current_user


router = APIRouter()


@router.post("/", response_model=schemas.Chapter)
def create_chapter(
    subject_id: int = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    chapter = schemas.ChapterCreate(name=name)
    db_chapter = services.chapters.create_chapter(db=db, chapter=chapter, subject_id=subject_id)
    
    if not db_chapter:
        raise HTTPException(status_code=400, detail="Subject not found")
    return db_chapter

@router.get("/", response_model=List[schemas.ChapterBase])
def read_all_chapters(
    limit: Optional[int] = Form(10),
    name: Optional[str] = Form(None), 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    chapters = services.chapters.get_all_chapters(db, limit=limit, name=name)
    return chapters


@router.get("/subject/{subject_id}", response_model=List[schemas.ChapterData])
async def get_chapters_by_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    chapters = services.chapters.get_chapters_by_subject(db, subject_id)
    if not chapters:
        raise HTTPException(status_code=404, detail="Chapters not found")
    return chapters








# @router.get("/{chapter_id}", response_model=schemas.Chapter)
# def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
#     db_chapter = services.chapters.get_chapter(db=db, chapter_id=chapter_id)
#     if db_chapter is None:
#         raise HTTPException(status_code=404, detail="Chapter not found")
#     return db_chapter