docker-env-up:
	docker compose --profile env up -d

docker-env-down:
	docker compose --profile env down

docker-env-clean:
	docker compose --profile env down -v

docker-app-up:
	docker compose --profile app up -d

docker-app-down:
	docker compose --profile app down

docker-app-clean:
	docker compose --profile app down -v

migrate:
	python3 -m alembic upgrade head

revert:
	python3 -m alembic downgrade base

format:
	ruff format

mypy:
	mypy .

ruff:
	ruff check

lint: mypy ruff
