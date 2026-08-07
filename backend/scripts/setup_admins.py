import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def setup():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        hashed_pw = get_password_hash("workshop2026")
        for user in users:
            user.password_hash = hashed_pw
        db.commit()
        print("Admin passwords successfully hashed and updated.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup()