from pydantic import BaseModel, EmailStr


class AccessTokenResponse(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserUpdatePasswordRequest(BaseModel):
    password: str


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
