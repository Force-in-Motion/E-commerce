from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from app.core import db_connector
from app.tools import HTTPErrors, UserRole
from app.api.depends.user import UserAuth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/login")

async def admin_guard(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
):
    user = await UserAuth.get_current_user_by_access(token, session)

    if user.role != UserRole.admin:
        raise HTTPErrors.not_admin
