FROM python:3.13-alpine

ENV ALEMBIC_VERSION=1.15.0
ENV ASYNCPG_VERSION=0.30.0

RUN pip install alembic==$ALEMBIC_VERSION asyncpg==$ASYNCPG_VERSION

RUN adduser -D migration && \
    mkdir -p /home/migration/app && \
    chown migration:migration /home/migration/app
WORKDIR /home/migration/app

COPY alembic.ini alembic.ini
COPY alembic/ alembic/
COPY domain/repositories domain/repositories

ENTRYPOINT ["python3", "-m", "alembic", "upgrade", "head"]
