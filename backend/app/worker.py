import os
import time
from celery import Celery

celery_app = Celery(
    "logistics_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True, max_retries=3)
def process_code_submission(self, submission_id: int, object_key: str):
    print(f"[WORKER] Picked up submission {submission_id}. Object Key: {object_key}")
    
    try:
        # TODO: 
        time.sleep(5)
        
        print(f"[WORKER] Successfully processed submission {submission_id}")
        return {"status": "success", "submission_id": submission_id}
        
    except Exception as exc:
        print(f"[WORKER] Failed to process submission {submission_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=10)