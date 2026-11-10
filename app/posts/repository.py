from sqlalchemy.orm import Session

from app.posts.models import Post


def create_post(session: Session, author_id: int, image_url: str, caption: str) -> Post:
    post = Post(author_id=author_id, image_url=image_url, caption=caption)
    session.add(post)
    session.flush()
    return post


def get_post_by_id(session: Session, post_id: int) -> Post | None:
    return session.get(Post, post_id)
