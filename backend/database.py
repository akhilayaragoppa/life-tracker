from supabase import create_client, Client
from config import get_settings
from models import InboxItem, Task, Goal, ClassificationResult
from typing import List, Optional
from datetime import datetime


class Database:
    def __init__(self):
        settings = get_settings()
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    # Inbox operations
    def add_to_inbox(self, raw_text: str, classification: ClassificationResult) -> InboxItem:
        data = {
            "raw_text": raw_text,
            "classification": classification.model_dump(),
            "processed": False,
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("inbox").insert(data).execute()
        return InboxItem(**result.data[0])

    def get_inbox_items(self, processed: Optional[bool] = None) -> List[InboxItem]:
        query = self.client.table("inbox").select("*").order("created_at", desc=True)

        if processed is not None:
            query = query.eq("processed", processed)

        result = query.execute()
        return [InboxItem(**item) for item in result.data]

    def mark_inbox_processed(self, inbox_id: str) -> None:
        self.client.table("inbox").update({"processed": True}).eq("id", inbox_id).execute()

    # Task operations
    def create_task(self, task: Task) -> Task:
        data = task.model_dump(exclude={"id", "created_at", "updated_at"})
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()

        result = self.client.table("tasks").insert(data).execute()
        return Task(**result.data[0])

    def get_tasks(
        self,
        urgency_bucket: Optional[str] = None,
        completed: Optional[bool] = None,
        linked_goal_id: Optional[str] = None
    ) -> List[Task]:
        query = self.client.table("tasks").select("*").order("created_at", desc=True)

        if urgency_bucket:
            query = query.eq("urgency_bucket", urgency_bucket)
        if completed is not None:
            query = query.eq("completed", completed)
        if linked_goal_id:
            query = query.eq("linked_goal_id", linked_goal_id)

        result = query.execute()
        return [Task(**task) for task in result.data]

    def update_task(self, task_id: str, updates: dict) -> Task:
        updates["updated_at"] = datetime.utcnow().isoformat()
        result = self.client.table("tasks").update(updates).eq("id", task_id).execute()
        return Task(**result.data[0])

    def complete_task(self, task_id: str) -> Task:
        return self.update_task(task_id, {"completed": True})

    # Goal operations
    def create_goal(self, goal: Goal) -> Goal:
        data = goal.model_dump(exclude={"id", "created_at", "updated_at"})
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()

        result = self.client.table("goals").insert(data).execute()
        return Goal(**result.data[0])

    def get_goals(self) -> List[Goal]:
        result = self.client.table("goals").select("*").order("created_at", desc=True).execute()
        return [Goal(**goal) for goal in result.data]

    def update_goal(self, goal_id: str, updates: dict) -> Goal:
        updates["updated_at"] = datetime.utcnow().isoformat()
        result = self.client.table("goals").update(updates).eq("id", goal_id).execute()
        return Goal(**result.data[0])

    def update_goal_progress(self, goal_id: str) -> Goal:
        # Calculate progress based on completed tasks
        tasks = self.get_tasks(linked_goal_id=goal_id)
        if not tasks:
            progress = 0.0
        else:
            completed = sum(1 for t in tasks if t.completed)
            progress = (completed / len(tasks)) * 100

        return self.update_goal(goal_id, {"progress": progress})
