from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.users.models import User


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("char_length(caption) <= 2200", name="ck_posts_caption_length"),
        CheckConstraint(
            "char_length(image_url) <= 2048", name="ck_posts_image_url_length"
        ),
        Index("ix_posts_author_id_created_at_id", "author_id", "created_at", "id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    author_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="RESTRICT")
    )
    image_url: Mapped[str] = mapped_column(Text)
    caption: Mapped[str] = mapped_column(Text, server_default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    author: Mapped["User"] = relationship()
