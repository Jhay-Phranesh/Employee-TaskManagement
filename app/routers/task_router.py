from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskAssign, TaskUpdate
from app.services.task_service import assign_task_to_employee

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task_id": new_task.id
    }


@router.get("/")
def get_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()


@router.post("/assign")
def assign_task(
    task_data: TaskAssign,
    db: Session = Depends(get_db)
):
    return assign_task_to_employee(
        task_data.task_id,
        task_data.employee_id,
        db
    )

@router.put("/{task_id}/status")
def update_task_status(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = task_update.status

    db.commit()

    return {
        "message": "Status updated successfully"
    }