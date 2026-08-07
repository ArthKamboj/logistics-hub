from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, get_db
from app.routers import auth
from app.auth import get_current_user
from app.models import User

app = FastAPI(title="Logistics Hub API", version="1.0.0")

app.include_router(auth.router)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Infrastructure health check. Verifies both API up-time and database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/api/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Protected route. Requires a valid JWT to access.
    """
    return {"username": current_user.username, "role": current_user.role, "email": current_user.email}