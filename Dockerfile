# Base pinada por digest para builds reproduzíveis.
# Atualize com:
#   docker pull python:3.13-slim
#   docker image inspect python:3.13-slim --format '{{index .RepoDigests 0}}'
FROM python:3.13-slim@sha256:2d44738ebf4ce5f63b9d9ea871e9c7cfdc0426f7b0c97cac915fd88ded1d86bb AS build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY career.md ./
COPY src ./src

# O build também valida o career.md e o HTML gerado.
RUN python3 src/build.py \
    && python3 src/check.py \
    && chown -R 10001:10001 /app

FROM python:3.13-slim@sha256:2d44738ebf4ce5f63b9d9ea871e9c7cfdc0426f7b0c97cac915fd88ded1d86bb AS runtime

ARG VERSION=dev
ARG REVISION=unknown

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    HOME=/home/app

# Usuário sem privilégios; o shell existe apenas para debug via container-shell.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home --shell /usr/sbin/nologin app

COPY --from=build --chown=10001:10001 /app /app

WORKDIR /app

USER 10001:10001

EXPOSE 8000

LABEL org.opencontainers.image.title="career-path" \
      org.opencontainers.image.description="Preview local do plano de carreira" \
      org.opencontainers.image.source="https://github.com/grazielevasconcelos/career-path" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}" \
      org.opencontainers.image.base.name="python:3.13-slim" \
      org.opencontainers.image.base.digest="sha256:2d44738ebf4ce5f63b9d9ea871e9c7cfdc0426f7b0c97cac915fd88ded1d86bb"

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)"]

STOPSIGNAL SIGTERM

CMD ["python3", "src/watch.py"]
