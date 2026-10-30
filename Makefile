PY := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.DEFAULT_GOAL := help

.PHONY: help build check test run clean

help: ## Mostra os comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

build: ## Gera o site em dist/
	$(PY) src/build.py

check: build ## Valida o career.md e o site gerado
	$(PY) src/check.py

test: check ## Atalho para build + validação

run: build ## Preview local com rebuild automático
	$(PY) src/watch.py

clean: ## Remove o site gerado
	rm -rf dist
