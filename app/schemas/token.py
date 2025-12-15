from pydantic import BaseModel
from typing import Optional



class RefreshCreate(BaseModel):
    token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
