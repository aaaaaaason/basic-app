
.PHONY: compose-up
compose-up:
	docker-compose up -d

.PHONY: compose-down
compose-down:
	docker-compose down

.PHONY: yapf
yapf:
	yapf -ir src

.PHONY: test
test:
	pytest src/basic_app/*

.PHONY: alembic-autogen
alembic-autogen:
	alembic revision --autogenerate -m "$(MSG)"
