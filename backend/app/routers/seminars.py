from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SeminarHall, User
from app.schemas import SeminarHallCreate, SeminarHallResponse
from app.auth import get_current_user

router = APIRouter(prefix="/seminars", tags=["Seminar Halls"])

@router.post("/", response_model=SeminarHallResponse, status_code=status.HTTP_201_CREATED)
def create_hall(hall: SeminarHallCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_hall = SeminarHall(**hall.model_dump())
    db.add(new_hall)
    db.commit()
    db.refresh(new_hall)
    return new_hall

@router.get("/", response_model=List[SeminarHallResponse])
def get_halls(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(SeminarHall).all()

@router.put("/{hall_id}/status", response_model=SeminarHallResponse)
def update_hall_status(hall_id: int, is_available: bool, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    hall = db.query(SeminarHall).filter(SeminarHall.id == hall_id).first()
    if not hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seminar hall not found")
    
    hall.is_available = is_available
    db.commit()
    db.refresh(hall)
    return hall