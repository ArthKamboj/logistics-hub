from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, get_db

app = FastAPI(title="Logistics Hub API", version="1.0.0")

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