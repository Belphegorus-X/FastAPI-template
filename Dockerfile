FROM python:3.13-alpine AS builder

ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/.poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry==$POETRY_VERSION

RUN adduser -D builder && \
    mkdir -p /home/builder/app && \
    chown builder:builder /home/builder/app
WORKDIR /home/builder/app
USER builder

COPY pyproject.toml poetry.lock ./

RUN if [[ -z "${INSTALL_DEBUGPY}" ]]; then \
        poetry install --no-root; \
    else \
        poetry install --no-root --with debug; \
    fi

FROM python:3.13-alpine AS runtime

EXPOSE 8000

RUN adduser -D runtime && \
    mkdir -p /home/runtime/app && \
    chown runtime:runtime /home/runtime/app
WORKDIR /home/runtime/app
USER runtime

ENV VIRTUAL_ENV=.venv \
    PATH=/home/runtime/app/.venv/bin:$PATH

COPY --from=builder /home/builder/app/${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

ENTRYPOINT ["sh", "-c", "PYTHONPATH=/home/runtime/app python apps/api/src/main.py"]
