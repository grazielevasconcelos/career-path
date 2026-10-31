# AGENTS.md

## Project overview

Static career-plan site for Graziele Vasconcelos, built with the NOW / NEXT /
LATER framework and published to GitHub Pages.

`career.md` is the single source of truth. A Python script (standard library
only) parses the Markdown and generates a static timeline in `dist/`. GitHub
Actions publishes `dist/` on every push to `main`.

```text
career.md  →  src/build.py  →  dist/  →  GitHub Actions  →  GitHub Pages
```

Stack:

- Python 3.9+ with the standard library only; there are no dependencies to install.
- Vanilla HTML, CSS, and JavaScript; no framework, bundler, or CDN.
- Docker/Podman is optional and only used for the local preview.

## Quick commands

```bash
make run      # preview with auto-rebuild at http://127.0.0.1:8000
make test     # build + validation; required before finishing any change
make build    # generate dist/
make check    # validate career.md and the generated HTML
make clean    # remove dist/
PORT=8001 make run
```

Container preview (optional):

```bash
make container-up        # foreground preview
make container-rebuild   # rebuild image and start
make container-test      # build + validation inside the hardened image
make container-down
```

For Podman, pass `ENGINE=podman`; for standalone `podman-compose`, also pass
`COMPOSE="podman-compose"`. See `docs/containers.md`.

## Repository map

- `career.md` — source of truth: front matter, lanes, and checklist items.
- `src/build.py` — parser, validation, and static HTML generation.
- `src/check.py` — validates `career.md` and invariants in the generated site.
- `src/watch.py` — local preview server with rebuild on file changes.
- `src/template.html` — page skeleton with `{{PLACEHOLDER}}` tokens.
- `src/styles.css` — themes, timeline, responsive layout, and print rules.
- `src/app.js` — filters, search, theme toggle, URL state, and print guide.
- `src/fonts/` — bundled Inter variable font and OFL license.
- `dist/` — generated artifact, gitignored; never edit or commit it.
- `docs/` — editing, container, and site usage guides.
- `.github/workflows/pages.yml` — CI build and GitHub Pages deployment.

## Editing rules

### career.md

- Keep the front matter block with `titulo`, `nome`, `cargo`, `resumo`, and
  `atualizado` (`YYYY-MM-DD`).
- Keep the three lanes exactly as `## NOW`, `## NEXT`, and `## LATER`.
- Item format: `- [ ] **001 · Name**`, with a unique ID of at least three digits.
- Allowed fields: `tipo`, `prioridade`, `prazo`, `link`, `tags`, `notas`,
  `evidencia`. `tipo` is required; `prioridade` must be `Alta`, `Média`, or
  `Baixa`.
- Mark completion with `[x]`; never add `status` or `concluido` fields.
- Update `atualizado` whenever the plan changes.
- When adding or removing a field, update `ALLOWED_FIELDS` in `src/build.py`,
  `src/check.py` if needed, and `docs/edicao.md`.

### Python

- Use only the standard library and keep Python 3.9 compatibility.
- Keep type hints, `PlanError`, and clear error messages with the offending
  `career.md` line number.
- Keep user-facing text, docstrings, and comments in Portuguese (pt-BR) to match
  the existing code.

### Template, build, and validation

- Every `{{PLACEHOLDER}}` in `src/template.html` must be replaced by
  `src/build.py`; unresolved placeholders are a build error.
- When adding a required element or structural invariant, update `src/check.py`
  in the same change.
- Do not bypass validation to make a broken plan build.

### Front-end

- Use semantic HTML, visible focus states, `aria-*` labels, the skip link, and
  reduced-motion support. Keep the interface usable with keyboard and screen
  readers.
- Keep UI copy in pt-BR.
- Do not add CDNs, external fonts, or runtime dependencies; the Inter font is
  already bundled in `src/fonts/`.
- Keep filters in the URL (`tipo`, `tag`, `q`) and persist theme/print-guide
  preferences in `localStorage` (`career-theme`, `career-print-guide`).
- Preserve light/dark themes and the print behavior: A4 portrait, always light
  output, colors enabled, and active filters respected. Update
  `docs/site.md` if this behavior changes.

### Containers and CI

- Keep the base image pinned by digest and update both `FROM` stages together.
  Follow the procedure in `docs/containers.md`.
- Keep the runtime nonroot (UID/GID `10001`), with a read-only root filesystem,
  `cap_drop: ALL`, `no-new-privileges`, and resource limits. Do not relax
  hardening without justification.
- `.github/workflows/pages.yml` runs `make test` on Python 3.12 and uploads
  `dist/`. Do not commit build artifacts or add steps that require secrets.

## Commits

Use Conventional Commits with an imperative description in Portuguese:

```text
feat(print): adiciona guia antes da impressão
fix: corrige contador de progresso
docs: divide README em guias por público
chore: atualiza imagem base
```

Keep the subject short and do not end it with a period.

## Definition of done

- `make test` passes.
- Visual changes are checked in the local preview.
- `career.md` and the relevant docs are updated when data or behavior changes.
- No generated files from `dist/` are edited or committed.

## Avoid

- Editing or versioning `dist/`.
- Adding npm/Node, bundlers, frameworks, or external CDN assets.
- Adding `career.md` fields without updating the parser, validator, and docs.
- Committing `tmp/`, `.venv/`, `prompts/`, `__pycache__/`, or `*.pyc`.
