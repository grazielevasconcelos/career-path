# Preview com containers

[← Voltar ao README](../README.md)

## Requisitos

Docker com Compose v2 (padrão) ou Podman 4+ com `podman compose`/`podman-compose`.

## Comandos disponíveis

```bash
make container-up
```

Abre em `http://127.0.0.1:8000`. O repositório é montado somente leitura e o `dist/` fica em um volume nomeado; edições em `career.md` ou `src/` continuam disparando rebuild automático.

Para usar outra porta:

```bash
PORT=8001 make container-up
```

| Comando | O que faz |
|---|---|
| `make container-build` | Builda a imagem de preview |
| `make container-up` | Sobe o preview em foreground |
| `make container-rebuild` | Rebuilda a imagem e sobe o preview |
| `make container-logs` | Acompanha os logs |
| `make container-shell` | Abre um shell no container |
| `make container-test` | Roda build + validação dentro da imagem |
| `make container-down` | Para e remove o container |
| `make container-clean` | Remove container, volume e imagem |

## Podman

Como o padrão é Docker, os comandos acima funcionam sem parâmetros. Para Podman:

```bash
make container-up ENGINE=podman
```

Se o ambiente usa o `podman-compose` standalone em vez do `podman compose`:

```bash
make container-up ENGINE=podman COMPOSE="podman-compose"
```

O `ENGINE` também vale para `container-build`, `container-test` e `container-clean`. O Compose usa `:Z` nos bind mounts para funcionar com SELinux no Podman; o Docker ignora quando não se aplica.

O runtime roda como UID `10001`; `career.md` e `src/` precisam ser legíveis por esse UID. Checkouts padrão do Git já atendem.

## Hardening

- Runtime nonroot com UID/GID `10001`.
- Root filesystem somente leitura; `/tmp` em `tmpfs` e apenas `dist/` em volume gravável.
- `cap_drop: [ALL]` e `no-new-privileges`.
- Limites de memória, CPU e PIDs; `stop_grace_period` com shutdown graceful via `SIGTERM`.
- Healthcheck no `Dockerfile` e validação de `career.md`/HTML durante o build.
- Base `python:3.13-slim` pinada por digest e labels OCI de título, source, versão e revisão.

O `dist/` do container fica no volume `career-dist`. Para gerar o artefato no host, use `make build`.

## Supply chain

Os comandos abaixo são opcionais e não fazem parte do `make` para manter compatibilidade com Docker e Podman:

```bash
# SBOM em SPDX (requer syft)
syft career-path:dev -o spdx-json > sbom.spdx.json

# Vulnerabilidades (requer trivy)
trivy image career-path:dev

# Docker Scout, quando disponível
docker scout cves career-path:dev
```

Assinatura e proveniência (cosign/SLSA) ficam fora do escopo deste preview local.

## Atualizar a base pinada

```bash
docker pull python:3.13-slim
docker image inspect python:3.13-slim --format '{{index .RepoDigests 0}}'
```

Atualize os dois `FROM` do `Dockerfile` e rode `make container-test`.
