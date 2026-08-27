from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth_router, project_router, employee_router, task_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Employee Task Management System",
    description="Employee Task Management API with JWT Authentication",
    version="1.0.0"
)

# Register Routers
app.include_router(auth_router.router)
app.include_router(project_router.router)
app.include_router(employee_router.router)
app.include_router(task_router.router)


@app.get("/")
def home():
    return {
        "message": "Employee Task Management API is running"
    }