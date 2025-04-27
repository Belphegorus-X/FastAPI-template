# FastAPI template: Chat application

## Local Build

Requirements:

* Python
* Poetry
* Docker

Install dependencies:
```bash
poetry install --no-root
```

Activate virtual environment
```bash
eval $(poetry env activate)
```

Run Postgres in docker and do migration using this command:

```bash
make docker-env-up
```

Run python application:

```bash
python3 -m apps.api.src.main
```

## Docker Build


Requirements:

* Docker

Use this command to set up Postgres database with migrations and run application:

```bash
make docker-app-up
```

## Migrations

Do migrations

```bash
make migrate
```

Revert migrations

```bash
make revert
```

## Pre-commit

Install pre-commit

```bash
pre-commit install --install-hooks
```

## Running tests

```bash
pytest
```
