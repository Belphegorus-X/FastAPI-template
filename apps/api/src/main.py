import json
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.websockets import WebSocket

from apps.api.src.core.config import get_settings
from apps.api.src.endpoints.chat.endpoints import router
from apps.api.src.endpoints.chat.models import ChatEventType, NewMessageEvent, ReadMessageEvent
from domain.domain_errors import DomainError

app = FastAPI(
    title="FastAPI real-time chat",
    version="0.1.0",
    description="Simple real-time chat",
    openapi_url="/openapi.json",
    docs_url="/",
)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError):
    logging.info(exc.inner_message)
    return JSONResponse(
        status_code=exc.status_code, content={"code": exc.code, "message": exc.message}
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        event = json.loads(text)
        event_type = ChatEventType(event["event_type"])

        match event_type:
            case ChatEventType.send:
                message = NewMessageEvent.model_validate_json(event["data"])
                print("message", message.text)
            case ChatEventType.read:
                message = ReadMessageEvent.model_dump_json(event["data"])
                print("read", message.chat_id)


app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().security.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=get_settings().security.allowed_hosts,
)


def main():
    config = get_settings()

    uvicorn.run(
        "main:app",
        host=config.http.hostname,
        port=config.http.port,
        reload=config.http.reload,
    )


if __name__ == "__main__":
    main()
