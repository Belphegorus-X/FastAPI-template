import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.websockets import WebSocket

from apps.api.src.core.config import get_settings
from apps.api.src.endpoints.auth.endpoints import auth_router
from apps.api.src.endpoints.chat.endpoints import chat_router
from apps.api.src.endpoints.chat.events import ChatEvents, ChatEventType
from apps.api.src.endpoints.user.endpoints import user_router
from domain.domain_errors import DomainError

app = FastAPI(
    title="FastAPI real-time chat",
    version="0.1.0",
    description="Simple real-time chat",
    openapi_url="/openapi.json",
    docs_url="/",
)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    logging.info(exc.inner_message)
    return JSONResponse(status_code=exc.status_code, content={"code": exc.code, "message": exc.message})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        event = ChatEvents.model_validate_json(text)  # type: ignore[attr-defined]

        match event.event_type:
            case ChatEventType.send:
                print("message", event.data.text)
            case ChatEventType.read:
                print("Read", event.data.chat_id)


app.include_router(chat_router)
app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).rstrip("/") for origin in get_settings().security.backend_cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=get_settings().security.allowed_hosts,
)


def main() -> None:
    config = get_settings()

    uvicorn.run(
        "apps.api.src.main:app",
        host=config.http.hostname,
        port=config.http.port,
        reload=config.http.reload,
    )


if __name__ == "__main__":
    main()
