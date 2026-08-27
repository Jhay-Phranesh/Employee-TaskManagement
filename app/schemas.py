from pydantic import BaseModel


# =====================
# User Schemas
# =====================

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    project_id: int


class UserLogin(BaseModel):
    username: str
    password: str


# =====================
# Project Schemas
# =====================

class ProjectCreate(BaseModel):
    project_name: str


# =====================
# Task Schemas
# =====================

class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int


class TaskAssign(BaseModel):
    task_id: int
    employee_id: int


class TaskUpdate(BaseModel):
    status: str
