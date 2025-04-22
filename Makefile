.PHONY: linter
linter: ## Run linter On Machine
linter:
	@printf "$(COLOR_GREEN)\nRunning tests$(COLOR_DEFAULT)\n\n"
	uv run python3 -m isort ./flaskr ./tests
	uv run python3 -m ruff format .
	uv run python3 -m flake8 --count ./
	uv run python3 -m mypy flaskr
