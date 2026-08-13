from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SeminarHall, Seminar, User
from app.schemas import SeminarHallCreate, SeminarHallResponse, SeminarCreate, SeminarResponse
from app.auth import get_current_user

router = APIRouter(prefix="/seminars", tags=["Seminars & Halls"])

@router.post("/halls", response_model=SeminarHallResponse, status_code=status.HTTP_201_CREATED)
def create_hall(
    hall: SeminarHallCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_hall = SeminarHall(**hall.model_dump())
    db.add(new_hall)
    db.commit()
    db.refresh(new_hall)
    return new_hall

@router.get("/halls", response_model=List[SeminarHallResponse])
def get_halls(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(SeminarHall).all()

@router.put("/halls/{hall_id}/status", response_model=SeminarHallResponse)
def update_hall_status(
    hall_id: int, 
    is_available: bool, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    hall = db.query(SeminarHall).filter(SeminarHall.id == hall_id).first()
    if not hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seminar hall not found")
    
    hall.is_available = is_available
    db.commit()
    db.refresh(hall)
    return hall



@router.post("/", response_model=SeminarResponse, status_code=status.HTTP_201_CREATED)
def create_seminar(
    seminar: SeminarCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hall = db.query(SeminarHall).filter(SeminarHall.id == seminar.hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seminar hall not found"
        )
        
    if not hall.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This hall is currently not available for bookings"
        )

    new_seminar = Seminar(
        title=seminar.title,
        description=seminar.description,
        hall_id=seminar.hall_id,
        start_time=seminar.start_time,
        end_time=seminar.end_time,
        created_by=current_user.id
    )
    
    db.add(new_seminar)
    db.commit()
    db.refresh(new_seminar)
    return new_seminar

@router.get("/", response_model=List[SeminarResponse])
def get_all_seminars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Seminar).all()