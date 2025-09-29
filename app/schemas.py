from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class GenerateResponse(BaseModel):
    success: bool
    content: str | None = None
    error: str | None = None

class GenerateRequest(BaseModel):
    prompt: str
    images: Optional[List[str]] = None 

class ContentBase(BaseModel):
    title: str
    content: str
    is_posted: Optional[bool] = False

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_posted: Optional[bool] = False

class ContentOut(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class SuccessSchema(BaseModel): 
    success: bool

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    role: str
    status: Optional[str] = "Activate"

class UserEdit(BaseModel):
    email: EmailStr
    username: str
    id: int
    role: str
    password: Optional[str] = None
    status: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        form_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str
    email: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
