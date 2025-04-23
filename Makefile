.PHONY: linter
linter: ## Run linter On Machine
linter:
	@printf "$(COLOR_GREEN)\nRunning tests$(COLOR_DEFAULT)\n\n"
	uv run ruff format .
	# uv run mypy .  # Check typing annotations as well as syntax errors
	uv run ruff check .

