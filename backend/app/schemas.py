from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

    
class SeminarHallBase(BaseModel):
    name: str
    capacity: int
    is_available: bool = True

class SeminarHallCreate(SeminarHallBase):
    pass

class SeminarHallResponse(SeminarHallBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    status: str = "pending"

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)