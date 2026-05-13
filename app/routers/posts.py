
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead


router = APIRouter(prefix="/posts", tags=["posts"])

@router.get('/', response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))
    return result.scalars().all()

@router.post('/', response_model=PostCreate, status_code=201)
async def create_post(data: PostCreate, session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@router.put('/{post_id}', response_model=PostRead)
async def update_post(post_id: str, data: PostCreate, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    post.sqlmodel_update(data.model_dump())
    await session.commit()
    await session.refresh(post)
    return post

@router.delete('/{post_id}', status_code=204)
async def delete_post(post_id: str, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)
    await session.delete(post)
    await session.commit()