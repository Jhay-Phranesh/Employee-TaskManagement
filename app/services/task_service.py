from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.logger import logger
from app.models import Task, User


def assign_task_to_employee(
    task_id: int,
    employee_id: int,
    db: Session
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    employee = db.query(User).filter(
        User.id == employee_id
    ).first()

    logger.warning(
    f"Project mismatch. Task Project={task.project_id}, Employee Project={employee.project_id}"
    )
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Business Validation
    if task.project_id != employee.project_id:
        raise HTTPException(
            status_code=400,
            detail="Project mismatch. Employee belongs to a different project."
        )

    task.assigned_to = employee.id

    db.commit()

    return {
        "message": "Task assigned successfully"
    }
