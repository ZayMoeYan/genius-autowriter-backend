from sqlalchemy.orm import Session
from app import models, schemas
from app.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.User)
    if search:
        search = f"%{search.lower()}%"
        query = query.filter(
            (models.User.username.ilike(search)) | (models.User.email.ilike(search))
        )
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        role=user_in.role,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_in: schemas.UserCreate):
    if user_in.username:
        db_user.username = user_in.username
    if user_in.email:
        db_user.email = user_in.email
    if user_in.password:
        db_user.hashed_password = get_password_hash(user_in.password)
    if user_in.role:
        db_user.role = user_in.role
    if user_in.status:
        db_user.status = user_in.status

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_content(db: Session, content_in: schemas.ContentCreate, user_id: int):
    db_content = models.Content(**content_in.dict(), user_id=user_id)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_user_contents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Content)
        .filter(models.Content.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_user_content(db: Session, content_id: int, user_id: int):
    return (
        db.query(models.Content)
        .filter(models.Content.id == content_id, models.Content.user_id == user_id)
        .first()
    )

def update_content(db: Session, db_content: models.Content, content_update: schemas.ContentUpdate):
    for key, value in content_update.dict(exclude_unset=True).items():
        setattr(db_content, key, value)
    db.commit()
    db.refresh(db_content)
    return db_content

def delete_content(db: Session, db_content: models.Content):
    db.delete(db_content)
    db.commit()
    return True
