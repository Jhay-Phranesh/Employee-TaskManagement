from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import hash_password
from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.auth import get_current_user
router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/")
def create_employee(
    employee: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_employee = User(
    username=employee.username,
    password=hash_password(employee.password),
    role=employee.role,
    project_id=employee.project_id
)

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee created successfully",
        "employee_id": new_employee.id
    }


@router.get("/")
def get_employees(
    db: Session = Depends(get_db)
):
    employees = db.query(User).all()

    return employees
