from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, ai
from app.deps import get_db, get_current_user
from typing import List
import re
import base64
from app.models import User

router = APIRouter(prefix="/contents", tags=["contents"])

@router.post("/api/generate", response_model=schemas.GenerateResponse)
async def generate(req: schemas.GenerateRequest):
    prompt = req.prompt
    images_data = []

    try:
        if req.images:
            for img_str in req.images:
                
                match = re.match(r"data:(.*?);base64,(.*)", img_str)
                if not match:
                    raise ValueError("Invalid base64 image string format")

                mime_type, b64data = match.groups()
                image_bytes = base64.b64decode(b64data)
                images_data.append((image_bytes, mime_type))

        generated = ai.generate_content(prompt, images_data)

        return {
            "success": True,
            "content": generated,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {e}")

@router.post("/", response_model=schemas.ContentOut)
def create_content(
    content_in: schemas.ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_content(db, content_in, user_id=current_user.id)

@router.get("/", response_model=List[schemas.ContentOut])
def list_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(current_user)
    return crud.get_user_contents(db, user_id=current_user.id)

@router.get("/{content_id}", response_model=schemas.ContentOut)
def get_one(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_content = crud.get_user_content(db, content_id, current_user.id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found or not yours")
    return db_content

@router.put("/{content_id}", response_model=schemas.ContentOut)
def update_one(
    content_id: int,
    content_in: schemas.ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_content = crud.get_user_content(db, content_id, current_user.id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found or not yours")
    return crud.update_content(db, db_content, content_in)

from fastapi import status

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_content = crud.get_user_content(db, content_id, current_user.id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found or not yours")

    return crud.delete_content(db, db_content)


