PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) warehouse_management:app

install:
	uv sync

dev:
	uv run flask --debug --app warehouse_management:app run

lint:
	uv run flake8 warehouse_management

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) warehouse_management:app
