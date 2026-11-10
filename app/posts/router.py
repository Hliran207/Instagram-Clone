from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostResponse
from app.posts.service import get_post, publish_post
from app.users.dependencies import CurrentUser

router = APIRouter(tags=["posts"])


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(user: CurrentUser, data: PostCreate, session: SessionDep) -> Post:
    return publish_post(session, user, data)


@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, session: SessionDep, _: CurrentUser) -> Post:
    return get_post(session, post_id)
