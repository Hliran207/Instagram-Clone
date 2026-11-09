from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.db import SessionDep
from app.core.errors import NotAuthenticatedError
from app.users.models import User
from app.users.repository import get_user_by_id

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    session: SessionDep,
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials, settings.jwt_secret, algorithms=["HS256"]
        )
    except jwt.InvalidTokenError as err:
        raise NotAuthenticatedError("Invalid or Expired token") from err
    user = get_user_by_id(session, int(payload["sub"]))
    if user is None:
        raise NotAuthenticatedError("Invalid or Expired token")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
