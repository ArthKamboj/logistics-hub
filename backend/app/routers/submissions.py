from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Submission, User
from app.schemas import SubmissionCreate, SubmissionResponse
from app.auth import get_current_user
from app.storage import get_presigned_put_url
import uuid

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.post("/request-upload", response_model=SubmissionResponse)
def request_upload_url(sub: SubmissionCreate, db: Session = Depends(get_db)):

    unique_id = str(uuid.uuid4())[:8]
    object_key = f"{sub.applicant_email}_{unique_id}.zip"
    
    db_sub = Submission(
        applicant_email=sub.applicant_email,
        language=sub.language,
        object_key=object_key
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    
    upload_url = get_presigned_put_url(object_key)
    
    response_data = SubmissionResponse.model_validate(db_sub)
    response_data.upload_url = upload_url
    return response_data

@router.put("/{submission_id}/confirm", response_model=SubmissionResponse)
def confirm_upload(submission_id: int, db: Session = Depends(get_db)):
    """
    Public endpoint to notify the system the file was successfully uploaded.
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    sub.status = "uploaded"
    db.commit()
    db.refresh(sub)
    return sub