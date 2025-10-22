.PHONY: help
help: # 도움말 출력
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*#' Makefile | sed -E 's/:.*#/\t- /' | sort
	@echo
	@echo "Usage: make <target>"

#------------------------------------------------------------------------
# DOCKER
#

DC=docker-compose -f docker-compose.yaml

.PHONY: build
build: # 도커 이미지 빌드
	$(DC) build --no-cache
	@echo "Docker images built successfully."

.PHONY: up
up: # 도커 컨테이너 실행
	$(DC) up -d

.PHONY: sh
sh: # 도커 컨테이너 쉘 접속
	$(DC) exec yt-stdl bash

.PHONY: down
down: # 도커 컨테이너 중지 및 제거
	$(DC) down

.PHONY: logs
logs: # 도커 컨테이너 로그 확인
	$(DC) logs -f

.PHONY: clean
clean: # 도커 이미지 및 컨테이너 정리
	$(DC) down --rmi all --volumes --remove-orphans
	@echo "Docker images and containers cleaned up."


#------------------------------------------------------------------------
# FORMAT & LINT
#------------------------------------------------------------------------

.PHONY: format
format: ## 코드 포맷팅 (Black 스타일)
	@echo "Formatting code with ruff..."
	uv run ruff format .
	@echo "Code formatted."

.PHONY: lint
lint: ## 코드 린트 검사
	@echo "Linting code with ruff..."
	uv run ruff check .
	@echo "Linting completed."

.PHONY: lint-fix
lint-fix: ## 코드 린트 검사 및 자동 수정
	@echo "Linting and fixing code with ruff..."
	uv run ruff check --fix .
	@echo "Linting and fixing completed."

.PHONY: check
check: lint format ## 전체 코드 품질 검사 및 포맷팅
	@echo "Code quality check completed."
