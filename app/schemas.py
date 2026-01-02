from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str | None
    likes: int
    username: str

    class Config:
        from_attributes = True
