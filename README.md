# career-path

Plano de carreira de **Graziele Vasconcelos**, construído com o framework **NOW / NEXT / LATER** e publicado no GitHub Pages.

**Página:** https://grazielevasconcelos.github.io/career-path/

## Como funciona

O [`career.md`](career.md) é a única fonte de verdade. Um script em Python (somente biblioteca padrão) lê o Markdown e gera uma timeline estática em `dist/`. O GitHub Actions publica essa pasta no Pages a cada push na `main`.

```text
career.md  →  src/build.py  →  dist/  →  GitHub Actions  →  GitHub Pages
```

Os rótulos qualitativos indicam o estágio de cada raia, sem prazos fixos:

- `NOW`: Agora
- `NEXT`: Próximo
- `LATER`: Depois

A página é **somente leitura**: para marcar um item como concluído, edite o `career.md`. O botão **Editar plano** abre o arquivo direto no editor do GitHub.

## Como editar

### 1. Cabeçalho

```markdown
---
titulo: Plano de Carreira
nome: Graziele Vasconcelos
cargo: Platform Engineer / SRE
resumo: Uma frase curta sobre o objetivo profissional.
atualizado: 2026-10-29
---
```

Atualize `atualizado` sempre que fizer uma mudança relevante. O formato é `AAAA-MM-DD`.

### 2. Itens

Cada item é um checklist com o ID e o nome em negrito, seguido dos campos aninhados:

```markdown
- [ ] **007 · Nome do item**
  - tipo: Curso
  - prioridade: Média
  - prazo: Mar/2027
  - link: https://exemplo.com
  - tags: cloud, kubernetes
  - notas: Critério para considerar o item concluído.
  - evidência: https://link-da-evidencia.com
```

| Campo | Obrigatório | Formato |
|---|---|---|
| `tipo` | Sim | Texto livre: `Certificação`, `Curso`, `Projeto` etc. |
| `prioridade` | Sim | `Alta`, `Média` ou `Baixa` |
| `prazo` | Não | Texto livre: `Dez/2026`, `1º trimestre/2027` etc. |
| `link` | Não | URL `http` ou `https` |
| `tags` | Não | Separadas por vírgula: `cloud, aws, iam` |
| `notas` | Não | Uma linha de texto |
| `evidência` | Não | URL ou texto que comprove a conclusão |

### 3. Concluir um item

Troque `[ ]` por `[x]`:

```markdown
- [x] **001 · AWS Certified Cloud Practitioner**
```

O card fica riscado, o contador geral e o contador da raia são atualizados automaticamente.

### 4. Adicionar um item

1. Escolha a raia (`NOW`, `NEXT` ou `LATER`).
2. Use o próximo ID disponível, com três dígitos.
3. Copie o modelo comentado no fim do `career.md`.
4. Preencha `tipo` e `prioridade`; os demais campos são opcionais.
5. Atualize a data do front matter.

## Preview local

Requisitos: Python 3.9+ e `make` (opcional).

```bash
make run
```

Abre em `http://127.0.0.1:8000`. O site é reconstruído ao salvar `career.md` ou os arquivos de `src/`.

Se a porta estiver ocupada, use `PORT=8001 make run`.

Sem `make`:

```bash
python3 src/build.py
python3 -m http.server -d dist 8000
```

Para validar sem subir servidor:

```bash
make test
```

## Preview com containers

Requisitos: Docker com Compose v2 (padrão) ou Podman 4+ com `podman compose`/`podman-compose`.

```bash
make container-up
```

Abre em `http://127.0.0.1:8000`. O repositório é montado somente leitura e o `dist/` fica em um volume nomeado; edições em `career.md` ou `src/` continuam disparando rebuild automático.

Para usar outra porta:

```bash
PORT=8001 make container-up
```

Comandos disponíveis:

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

### Hardening

- Runtime nonroot com UID/GID `10001`.
- Root filesystem somente leitura; `/tmp` em `tmpfs` e apenas `dist/` em volume gravável.
- `cap_drop: [ALL]` e `no-new-privileges`.
- Limites de memória, CPU e PIDs; `stop_grace_period` com shutdown graceful via `SIGTERM`.
- Healthcheck no `Dockerfile` e validação de `career.md`/HTML durante o build.
- Base `python:3.13-slim` pinada por digest e labels OCI de título, source, versão e revisão.

O `dist/` do container fica no volume `career-dist`. Para gerar o artefato no host, use `make build`.

### Supply chain

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

Para atualizar a base pinada:

```bash
docker pull python:3.13-slim
docker image inspect python:3.13-slim --format '{{index .RepoDigests 0}}'
```

Atualize os dois `FROM` do `Dockerfile` e rode `make container-test`.

## Publicação

O workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) roda em todo push na `main` e também pode ser disparado manualmente.

Na primeira vez, ative o Pages em **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Depois de qualquer edição:

```bash
git add career.md
git commit -m "Atualiza plano de carreira"
git push origin main
```

O site é atualizado em alguns minutos.

## Estrutura

```text
.
├── career.md                     # fonte única do plano
├── README.md
├── Dockerfile                    # imagem de preview com hardening
├── docker-compose.yml            # preview local em container
├── .dockerignore
├── Makefile
├── src/
│   ├── build.py                  # parser + gerador estático
│   ├── check.py                  # validação do plano e do HTML
│   ├── watch.py                  # preview com rebuild automático
│   ├── template.html             # estrutura da página
│   ├── styles.css                # visual claro/escuro, timeline e impressão
│   ├── app.js                    # filtros, busca, tema e guia de impressão
│   ├── fonts/
│   │   ├── Inter-Variable.woff2  # fonte Inter empacotada localmente
│   │   └── OFL.txt               # licença SIL Open Font License
│   └── favicon.svg
└── .github/workflows/pages.yml
```

`dist/` é gerado localmente e no CI; não é versionado.

## Filtros e tema

- Filtro por tipo, por tag e busca textual; os filtros combinam entre si.
- O estado dos filtros fica na URL, então é possível compartilhar uma visão filtrada.
- Tema claro por padrão; o botão de tema alterna para escuro e salva a preferência no navegador.

## Impressão / PDF

O botão **Imprimir / PDF** abre um guia com as opções recomendadas. A impressão
usa o layout A4 retrato do site, com cores, e respeita os filtros e a busca
ativos. No conteúdo atual, o resultado tem cerca de 2 páginas.

- O PDF é sempre claro, mesmo quando a página está no tema escuro.
- Desmarque **Cabeçalhos e rodapés** para remover data, título e URL do navegador.
- Marque **Gráficos de fundo** para manter as cores dos badges, raias e do anel
  de progresso.
- No celular, use a opção **Salvar como PDF**.
- A fonte Inter é empacotada localmente em `src/fonts/` (licença OFL), então o
  PDF embute a mesma fonte em Linux, Android, iOS e macOS.
- O link **Como imprimir** no rodapé reabre o guia. Marque "Não mostrar este
  guia novamente" para abrir a impressão do navegador diretamente nas próximas
  vezes.
- O cabeçalho e o rodapé do navegador não podem ser removidos por CSS; por isso
  o guia orienta a desativá-los.

## Problemas comuns

| Mensagem | O que fazer |
|---|---|
| `item inválido` | Confira o formato `- [ ] **001 · Nome**` |
| `campo desconhecido` | Use apenas os campos da tabela acima |
| `raia ausente` | Mantenha `## NOW`, `## NEXT` e `## LATER` |
| `ID duplicado` | Cada item precisa de um ID único |
| `prioridade ... deve ser` | Use `Alta`, `Média` ou `Baixa` |
| `não é uma URL http(s) válida` | Corrija o `link` ou a `evidência` |

O build mostra o número da linha com problema no `career.md`.
