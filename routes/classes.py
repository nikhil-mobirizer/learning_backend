from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from database import get_db
import services.classes
from services.auth import get_current_user  


router = APIRouter()

@router.post("/", response_model=schemas.Class)
def create_class(
    name: str = Form(...),
    tagline: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    class_ = schemas.ClassCreate(name=name, tagline=tagline)
    return services.classes.create_class(db=db, class_=class_)

@router.get("/all_data", response_model=List[schemas.ClassData])
def read_classes(
    limit: int = 1000,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    classes = services.classes.get_all_classes(db, limit=limit)
    
    return classes

@router.get("/", response_model=List[schemas.Class])
def read_all_classes(
    limit: Optional[int] = Form(10),
    name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),   
):
    classes = services.classes.get_all_classes(db, limit=limit, name=name)
    return classes


@router.get("/{class_id}", response_model=schemas.Class)
def read_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    db_class = services.classes.get_class(db=db, class_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

