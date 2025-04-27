from time import time
from uuid import UUID

import jwt
from pydantic import BaseModel

from apps.api.src.core.config import get_settings

JWT_ALGORITHM = "HS256"


class JWTTokenPayload(BaseModel):
    iss: str
    sub: str
    exp: int
    iat: int


class JWTToken(BaseModel):
    payload: JWTTokenPayload
    access_token: str


def create_jwt_token(user_id: UUID) -> JWTToken:
    iat = int(time())
    exp = iat + get_settings().security.jwt_access_token_expire_secs

    token_payload = JWTTokenPayload(
        iss=get_settings().security.jwt_issuer,
        sub=str(user_id),
        exp=exp,
        iat=iat,
    )

    access_token = jwt.encode(
        token_payload.model_dump(),
        get_settings().security.jwt_secret_key.get_secret_value(),
        algorithm=JWT_ALGORITHM,
    )

    return JWTToken(payload=token_payload, access_token=access_token)
