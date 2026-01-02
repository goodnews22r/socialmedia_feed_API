from sqlalchemy.orm import Session
from .models import User, Post



def create_user(db: Session, username: str, email: str):
    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )

    if existing_user:
        return None

    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_post(
    db: Session,
    user: User,
    title: str,
    content: str,
    image: str | None
):
    post = Post(
        title=title,
        content=content,
        image=image,
        likes=0,        # IMPORTANT
        user=user
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_posts(db: Session):
    return db.query(Post).all()


def get_user_posts(db: Session, username: str):
    return (
        db.query(Post)
        .join(User)
        .filter(User.username == username)
        .all()
    )


def like_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    post.likes += 1
    db.commit()
    db.refresh(post)
    return post
