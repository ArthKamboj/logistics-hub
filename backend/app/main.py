from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, get_db
from app.routers import auth, seminars, tasks, submissions 
from app.storage import ensure_bucket_exists
from app.auth import get_current_user
from app.models import User

app = FastAPI(title="Logistics Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    try:
        ensure_bucket_exists()
    except Exception as e:
        print(f"Failed to initialize MinIO bucket: {e}")

app.include_router(auth.router)
app.include_router(seminars.router)
app.include_router(tasks.router)
app.include_router(submissions.router)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.get("/api/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role, "email": current_user.email}