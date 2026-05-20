
from app.db.session import engine
from sqlmodel import SQLModel
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)