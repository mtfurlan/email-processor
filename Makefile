.DEFAULT_GOAL := run

.PHONY: python
python: .venv ## run python in venv
	.venv/bin/python

.PHONY: deps
deps: .venv ## install deps into venv

.venv: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	touch .venv # update .venv timestamp

.PHONY: run
run: .venv ## run the thing
	@.venv/bin/python runner.py

.PHONY: check
check: .venv ## run format/lint checks
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

.PHONY: fix
fix: .venv ## run format/lint fixer
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

.PHONY: help
help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

