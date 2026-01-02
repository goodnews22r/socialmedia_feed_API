import os
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
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
    }



@app.post("/posts/")
def create_new_post(
    username: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_path = None
    if image:
        image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())

    post = create_post(db, user, title, content, image_path)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "image": post.image,
        "likes": post.likes,
        "username": user.username
    }


@app.get("/posts/", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    posts = get_all_posts(db)
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "image": post.image,
            "likes": post.likes,
            "username": post.user.username
        }
        for post in posts
    ]


@app.get("/users/{username}/posts", response_model=list[PostResponse])
def list_user_posts(username: str, db: Session = Depends(get_db)):
    posts = get_user_posts(db, username)
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "image": post.image,
            "likes": post.likes,
            "username": username
        }
        for post in posts
    ]


@app.post("/posts/{post_id}/like")
def like_a_post(post_id: int, db: Session = Depends(get_db)):
    post = like_post(db, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "message": "Post liked",
        "likes": post.likes
    }
