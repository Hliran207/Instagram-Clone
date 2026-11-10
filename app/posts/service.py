from sqlalchemy.orm import Session

from app.core.errors import PostNotFoundError
from app.posts.models import Post
from app.posts.repository import create_post, get_post_by_id
from app.posts.schemas import PostCreate
from app.users.models import User


def publish_post(session: Session, author: User, data: PostCreate) -> Post:
    post = create_post(
        session,
        author_id=author.id,
        image_url=str(data.image_url),
        caption=data.caption,
    )
    session.commit()
    return post


def get_post(session: Session, post_id: int) -> Post:
    post = get_post_by_id(session, post_id)
    if post is None:
        raise PostNotFoundError("Post not found")
    return post
