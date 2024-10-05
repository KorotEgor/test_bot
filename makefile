install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

run:
	uv run bot

lint:
	uv run ruff format && uv run ruff check
