default: build

build:
	docker compose build --no-cache

deploy-local:
	docker compose up --build
