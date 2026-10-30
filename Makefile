PY := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

ENGINE ?= docker
COMPOSE ?= $(ENGINE) compose
IMAGE ?= career-path:dev
PORT ?= 8000
APP_VERSION ?= dev
REVISION ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo unknown)

export PORT APP_VERSION REVISION

.DEFAULT_GOAL := help

.PHONY: help build check test run clean \
	container-build container-up container-rebuild container-down \
	container-logs container-shell container-test container-clean

help: ## Mostra os comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

build: ## Gera o site em dist/
	$(PY) src/build.py

check: build ## Valida o career.md e o site gerado
	$(PY) src/check.py

test: check ## Atalho para build + validação

run: build ## Preview local com rebuild automático
	$(PY) src/watch.py

clean: ## Remove o site gerado
	rm -rf dist

container-build: ## Builda a imagem de preview
	$(ENGINE) build --pull \
		--build-arg VERSION=$(APP_VERSION) \
		--build-arg REVISION=$(REVISION) \
		-t $(IMAGE) .

container-up: ## Sobe o preview em container (foreground)
	@echo "Preview em http://127.0.0.1:$(PORT) (Ctrl+C para parar)"
	$(COMPOSE) up

container-rebuild: ## Rebuilda a imagem e sobe o preview
	@echo "Preview em http://127.0.0.1:$(PORT) (Ctrl+C para parar)"
	$(COMPOSE) up --build

container-down: ## Para e remove o container
	$(COMPOSE) down

container-logs: ## Acompanha os logs do preview
	$(COMPOSE) logs -f preview

container-shell: ## Abre um shell no container de preview
	$(COMPOSE) run --rm preview sh

container-test: container-build ## Roda build + validação dentro da imagem
	$(ENGINE) run --rm \
		--read-only \
		--tmpfs /tmp:rw,noexec,nosuid,nodev,size=16m \
		--cap-drop ALL \
		--security-opt no-new-privileges \
		--user 10001:10001 \
		$(IMAGE) python3 src/check.py

container-clean: ## Remove container, volume e imagem de preview
	-$(COMPOSE) down -v
	-$(ENGINE) rmi $(IMAGE)
