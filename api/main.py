from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import CaptureInput, InboxItem, Task, Goal
from classifier import LLMClassifier
from database import Database
from typing import List, Optional

app = FastAPI(title="Life Tracker API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = LLMClassifier()
db = Database()


@app.get("/")
def root():
    return {"message": "Life Tracker API", "status": "running"}


@app.post("/capture", response_model=InboxItem)
def capture(input: CaptureInput):
    """
    Main capture endpoint - accepts natural language text and classifies it.
    Zero friction: just send text, get back classified item in inbox.
    """
    try:
        # Classify using LLM
        classification = classifier.classify(input.text)

        # Add to inbox
        inbox_item = db.add_to_inbox(input.text, classification)

        return inbox_item
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        print(f"Capture error: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/inbox", response_model=List[InboxItem])
def get_inbox(processed: Optional[bool] = None):
    """
    Get inbox items. Filter by processed status if provided.
    """
    try:
        return db.get_inbox_items(processed=processed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inbox/{inbox_id}/process")
def process_inbox_item(inbox_id: str, action: str = "accept"):
    """
    Process an inbox item - convert to task/goal or dismiss.
    """
    try:
        inbox_items = db.get_inbox_items(processed=False)
        inbox_item = next((item for item in inbox_items if item.id == inbox_id), None)

        if not inbox_item:
            raise HTTPException(status_code=404, detail="Inbox item not found")

        if action == "accept":
            classification = inbox_item.classification

            if classification.item_type == "task":
                # Create task
                task = Task(
                    title=classification.title,
                    category=classification.category,
                    urgency_bucket=classification.timeline,
                    loose_deadline=classification.loose_deadline,
                    description=classification.description
                )
                created_task = db.create_task(task)
                db.mark_inbox_processed(inbox_id)
                return {"status": "created", "type": "task", "item": created_task}

            elif classification.item_type == "goal":
                # Create goal
                goal = Goal(
                    title=classification.title,
                    description=classification.description,
                    category=classification.category
                )
                created_goal = db.create_goal(goal)

                # Create suggested tasks if any
                created_tasks = []
                if classification.suggested_tasks:
                    for task_title in classification.suggested_tasks:
                        task = Task(
                            title=task_title,
                            category=classification.category,
                            urgency_bucket="bucket",
                            linked_goal_id=created_goal.id
                        )
                        created_tasks.append(db.create_task(task))

                db.mark_inbox_processed(inbox_id)
                return {
                    "status": "created",
                    "type": "goal",
                    "goal": created_goal,
                    "suggested_tasks": created_tasks
                }

        elif action == "dismiss":
            db.mark_inbox_processed(inbox_id)
            return {"status": "dismissed"}

        else:
            raise HTTPException(status_code=400, detail="Invalid action")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks", response_model=List[Task])
def get_tasks(
    urgency_bucket: Optional[str] = None,
    completed: Optional[bool] = None,
    linked_goal_id: Optional[str] = None
):
    """
    Get tasks with optional filters.
    """
    try:
        return db.get_tasks(urgency_bucket, completed, linked_goal_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, updates: dict):
    """
    Update task fields (e.g., urgency_bucket, title, etc.)
    """
    try:
        task = db.update_task(task_id, updates)
        return {"task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: str):
    """
    Mark a task as completed and update linked goal progress if applicable.
    """
    try:
        task = db.complete_task(task_id)

        # Update goal progress if task is linked to a goal
        if task.linked_goal_id:
            updated_goal = db.update_goal_progress(task.linked_goal_id)
            return {"task": task, "updated_goal": updated_goal}

        return {"task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/goals", response_model=List[Goal])
def get_goals():
    """
    Get all goals with their progress.
    """
    try:
        return db.get_goals()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
