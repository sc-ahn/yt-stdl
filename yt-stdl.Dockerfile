# 빌드 스테이지
FROM python:3.11.11-slim-bullseye AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY app ./app

# uv로 의존성 설치 (프로덕션만)
RUN uv sync --frozen --no-dev && \
    rm -rf ~/.cache/uv

# 실행 스테이지
FROM python:3.11.11-slim-bullseye
RUN groupadd -g 1000 huray && \
    useradd -u 1000 -g huray -d /huray/yt-stdl -m -s /bin/bash huray

WORKDIR /huray/yt-stdl

# 읽고 쓰기 가능한 리소스 디렉터리 (example)
COPY --chown=huray:huray example /huray/yt-stdl/example

# uv 가상환경 복사
COPY --chown=huray:huray --from=builder /app/.venv /huray/yt-stdl/.venv
COPY --chown=huray:huray --from=builder /app/app /huray/yt-stdl/app

# 가상환경 PATH 및 PYTHONPATH 설정
ENV PATH="/huray/yt-stdl/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/huray/yt-stdl/.venv"
ENV PYTHONPATH="/huray/yt-stdl:$PYTHONPATH"

USER huray
