import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.user import User
from app.models.post import Post
from app.schemas.user import UserCreate, UserRead
from app.schemas.post import PostRead


router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get('/{user_id}/posts', response_model=List[PostRead])
async def get_user_posts(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    result = await session.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()

@router.post('/', response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.put('/{user_id}', response_model=UserRead)
async def update_user(user_id: uuid.UUID, data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.sqlmodel_update(data.model_dump())
    await session.commit()
    await session.refresh(user)
    return user

@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()


