from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class CaptureInput(BaseModel):
    text: str


class ClassificationResult(BaseModel):
    item_type: Literal["goal", "task"]
    category: str
    timeline: Literal["today", "this_week", "this_month", "bucket"]
    title: str
    description: Optional[str] = None
    loose_deadline: Optional[str] = None
    suggested_tasks: Optional[list[str]] = None


class Goal(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: str
    progress: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Task(BaseModel):
    id: Optional[str] = None
    title: str
    category: str
    urgency_bucket: Literal["today", "this_week", "this_month", "bucket"]
    loose_deadline: Optional[str] = None
    linked_goal_id: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InboxItem(BaseModel):
    id: Optional[str] = None
    raw_text: str
    classification: ClassificationResult
    processed: bool = False
    created_at: Optional[datetime] = None
