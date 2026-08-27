from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.logger import logger
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = Project(
        project_name=project.project_name
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    logger.info(
    f"Project created: {new_project.project_name}"
    )

    return {
        "message": "Project created successfully",
        "project_id": new_project.id
    }


@router.get("/")
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(Project).all()

    return projects