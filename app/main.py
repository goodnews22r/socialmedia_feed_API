import os
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .crud import (
    create_user,
    get_user,
    create_post,
    get_all_posts,
    get_user_posts,
    like_post
)
from .schemas import UserCreate, PostResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Social Media Feed API")
\

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.username, user.email)

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
