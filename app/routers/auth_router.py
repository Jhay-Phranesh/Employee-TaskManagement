from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    hash_password,
    verify_password
)
from app.database import get_db
from app.logger import logger
from app.models import User
from app.schemas import UserCreate, UserLogin

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role,
        project_id=user.project_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"User registered: {new_user.username}"
    )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        data={
            "sub": db_user.username,
            "role": db_user.role
        }
    )

    logger.info(
        f"User logged in: {db_user.username}"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }