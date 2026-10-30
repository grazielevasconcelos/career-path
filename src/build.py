#!/usr/bin/env python3
"""Gera a página estática do plano de carreira a partir de plan.md.

O arquivo plan.md é a única fonte de verdade. Este script usa apenas a
biblioteca padrão do Python: não há dependências para instalar.
"""

from __future__ import annotations

import html
import math
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
PLAN = ROOT / "plan.md"

REPO = "grazielevasconcelos/career-path"
REPO_URL = f"https://github.com/{REPO}"
EDIT_URL = f"{REPO_URL}/edit/main/plan.md"
PAGE_URL = "https://grazielevasconcelos.github.io/career-path/"

LANES = {
    "NOW": {"label": "Agora", "class": "lane-now"},
    "NEXT": {"label": "Próximo", "class": "lane-next"},
    "LATER": {"label": "Depois", "class": "lane-later"},
}
ALLOWED_FIELDS = {"tipo", "prioridade", "link", "tags", "prazo", "notas", "evidencia"}
REQUIRED_FRONT = ("titulo", "nome", "cargo", "resumo", "atualizado")
ITEM_RE = re.compile(
    r"^\s*-\s*\[([ xX])\]\s*\*\*(\d{3,})\s*(?:·|—|-|\|)\s*(.+?)\*\*\s*$"
)
FIELD_RE = re.compile(r"^\s{2,}-\s+([^:]+)\s*:\s*(.*)$")
LANE_RE = re.compile(r"^##\s+(NOW|NEXT|LATER)\s*$", re.IGNORECASE)

CHECK_ICON = (
    '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="m3.5 8.5 3 3 6-7" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
ARROW_ICON = (
    '<svg class="icon-sm" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path d="M5 11 11 5M6 5h5v5" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
CALENDAR_ICON = (
    '<svg class="icon-xs" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<rect x="2.5" y="3.5" width="11" height="10" rx="2" fill="none" '
    'stroke="currentColor" stroke-width="1.3"/>'
    '<path d="M5 2v3M11 2v3M2.5 7h11" fill="none" stroke="currentColor" '
    'stroke-width="1.3" stroke-linecap="round"/>'
    "</svg>"
)


class PlanError(Exception):
    """Erro de conteúdo ou formato no plan.md."""


def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.strip().lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"\s+", "_", value)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def read_plan_text(path: Path = PLAN) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PlanError(f"Arquivo não encontrado: {path}") from exc


def parse_front_matter(text: str) -> tuple[dict[str, str], list[tuple[int, str]]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise PlanError("O plan.md deve começar com um bloco de front matter delimitado por ---.")

    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise PlanError("Front matter sem fechamento ---.")

    front: dict[str, str] = {}
    for index in range(1, closing):
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise PlanError(f"Linha {index + 1}: front matter inválido. Use chave: valor.")
        key, value = raw.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key in front:
            raise PlanError(f"Linha {index + 1}: chave duplicada no front matter: {key}.")
        front[key] = value

    for key in REQUIRED_FRONT:
        if not front.get(key):
            raise PlanError(f"Front matter: campo obrigatório ausente ou vazio: {key}.")
    try:
        date.fromisoformat(front["atualizado"])
    except ValueError as exc:
        raise PlanError("Front matter: 'atualizado' deve estar no formato AAAA-MM-DD.") from exc

    body = list(enumerate(lines, start=1))[closing + 1 :]
    return front, body


def validate_url(value: str, item: dict, field: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise PlanError(
            f"Linha {item['line']}: {field} do item {item['id']} não é uma URL http(s) válida: {value}"
        )


def validate_item(item: dict) -> None:
    fields = item["fields"]
    tipo = fields.get("tipo", "").strip()
    if not tipo:
        raise PlanError(f"Linha {item['line']}: item {item['id']} sem o campo 'tipo'.")

    item["tipo"] = tipo
    item["type_slug"] = slugify(item["tipo"])

    priority_raw = fields.get("prioridade", "").strip()
    if not priority_raw:
        raise PlanError(f"Linha {item['line']}: item {item['id']} sem o campo 'prioridade'.")
    priority = normalize_key(priority_raw)
    priority_map = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}
    if priority not in priority_map:
        raise PlanError(
            f"Linha {item['line']}: prioridade do item {item['id']} deve ser Alta, Média ou Baixa."
        )
    item["prioridade"] = priority_map[priority]
    item["priority_slug"] = priority

    link = fields.get("link", "").strip()
    if link:
        validate_url(link, item, "link")
    item["link"] = link

    tags: list[str] = []
    for tag in fields.get("tags", "").split(","):
        tag = tag.strip()
        if tag and tag not in tags:
            tags.append(tag)
    item["tags"] = tags
    item["tag_slugs"] = [slugify(tag) for tag in tags]

    item["prazo"] = fields.get("prazo", "").strip()
    item["notas"] = fields.get("notas", "").strip()

    evidence = fields.get("evidencia", "").strip()
    if evidence.startswith(("http://", "https://")):
        validate_url(evidence, item, "evidência")
        item["evidence_url"] = evidence
        item["evidence_text"] = ""
    else:
        item["evidence_url"] = ""
        item["evidence_text"] = evidence

    item["search"] = " ".join(
        [
            item["id"],
            item["name"],
            item["tipo"],
            item["prioridade"],
            " ".join(tags),
            item["prazo"],
            item["notas"],
            evidence,
        ]
    ).lower()


def parse_plan(text: str) -> dict:
    front, body = parse_front_matter(text)
    lanes: dict[str, list[dict]] = {name: [] for name in LANES}
    seen_lanes: set[str] = set()
    current_lane: str | None = None
    current_item: dict | None = None
    in_comment = False

    for lineno, raw in body:
        line = raw.rstrip()
        stripped = line.strip()

        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                in_comment = True
            continue
        if not stripped:
            continue

        lane_match = LANE_RE.match(line)
        if lane_match:
            lane_name = lane_match.group(1).upper()
            if lane_name in seen_lanes:
                raise PlanError(f"Linha {lineno}: raia {lane_name} duplicada.")
            seen_lanes.add(lane_name)
            current_lane = lane_name
            current_item = None
            continue

        if line.lstrip().startswith("- ["):
            item_match = ITEM_RE.match(line)
            if not item_match:
                raise PlanError(
                    f"Linha {lineno}: item inválido. Use: - [ ] **001 · Nome do item**"
                )
            if current_lane is None:
                raise PlanError(f"Linha {lineno}: item fora de uma raia NOW/NEXT/LATER.")
            item = {
                "id": item_match.group(2),
                "name": item_match.group(3).strip(),
                "done": item_match.group(1).lower() == "x",
                "fields": {},
                "line": lineno,
            }
            if not item["name"]:
                raise PlanError(f"Linha {lineno}: o item precisa de um nome.")
            lanes[current_lane].append(item)
            current_item = item
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            if current_item is None:
                raise PlanError(f"Linha {lineno}: campo fora de um item.")
            raw_key = field_match.group(1).strip()
            key = normalize_key(raw_key)
            if key in {"status", "concluido"}:
                raise PlanError(
                    f"Linha {lineno}: o campo '{raw_key}' não é usado. "
                    "Marque a conclusão com [x] no início do item."
                )
            if key not in ALLOWED_FIELDS:
                raise PlanError(
                    f"Linha {lineno}: campo desconhecido '{raw_key}'. "
                    f"Campos aceitos: {', '.join(sorted(ALLOWED_FIELDS))}."
                )
            if key in current_item["fields"]:
                raise PlanError(
                    f"Linha {lineno}: campo '{key}' duplicado no item {current_item['id']}."
                )
            current_item["fields"][key] = field_match.group(2).strip()
            continue

        if re.match(r"^\s{2,}-\s+", line):
            raise PlanError(f"Linha {lineno}: campo inválido. Use '  - chave: valor'.")
        if re.match(r"^-\s+[^:\s]+\s*:", line):
            raise PlanError(
                f"Linha {lineno}: campo sem indentação. Use dois espaços antes de '- chave: valor'."
            )
        # Títulos, subtítulos e texto de apoio são ignorados.

    missing = [name for name in LANES if name not in seen_lanes]
    if missing:
        raise PlanError(
            f"Raia(s) ausente(s): {', '.join(missing)}. Use ## NOW, ## NEXT e ## LATER."
        )

    ids: dict[str, int] = {}
    for items in lanes.values():
        for item in items:
            validate_item(item)
            if item["id"] in ids:
                raise PlanError(
                    f"ID duplicado: {item['id']} (linhas {ids[item['id']]} e {item['line']})."
                )
            ids[item["id"]] = item["line"]

    return {"front": front, "lanes": lanes}


def render_type_filters(items: list[dict]) -> str:
    types: list[str] = []
    for item in items:
        if item["tipo"] not in types:
            types.append(item["tipo"])
    return "\n".join(
        f'<button class="segmented-button" type="button" data-type="{esc(slugify(kind))}" '
        f'aria-pressed="false">{esc(kind)}</button>'
        for kind in types
    )


def render_tag_filters(items: list[dict]) -> str:
    tags: dict[str, str] = {}
    for item in items:
        for tag, slug in zip(item["tags"], item["tag_slugs"]):
            tags.setdefault(slug, tag)
    return "\n".join(
        f'<button class="tag-chip" type="button" data-tag="{esc(slug)}" '
        f'aria-pressed="false">#{esc(tags[slug])}</button>'
        for slug in sorted(tags, key=lambda value: tags[value].lower())
    )


def render_links(item: dict) -> str:
    links: list[str] = []
    if item["link"]:
        links.append(
            f'<a class="item-link" href="{esc(item["link"])}" target="_blank" '
            f'rel="noopener noreferrer">Acessar {ARROW_ICON}</a>'
        )
    if item["evidence_url"]:
        links.append(
            f'<a class="item-evidence" href="{esc(item["evidence_url"])}" target="_blank" '
            f'rel="noopener noreferrer">Evidência {ARROW_ICON}</a>'
        )
    elif item["evidence_text"]:
        links.append(f'<span class="item-evidence">Evidência: {esc(item["evidence_text"])}</span>')
    if not links:
        return ""
    return f'<div class="item-links">{"".join(links)}</div>'


def render_card(item: dict, reveal_index: int) -> str:
    done_class = " is-done" if item["done"] else ""
    checked_class = " is-checked" if item["done"] else ""
    tags_html = "".join(f'<span class="tag">#{esc(tag)}</span>' for tag in item["tags"])
    deadline_html = (
        f'<span class="item-deadline">{CALENDAR_ICON}{esc(item["prazo"])}</span>'
        if item["prazo"]
        else ""
    )
    tags_block = f'<div class="item-tags">{tags_html}</div>' if tags_html else ""
    notes_block = f'<p class="item-notes">{esc(item["notas"])}</p>' if item["notas"] else ""
    delay = min(reveal_index * 55, 330)
    status = "Concluído" if item["done"] else "A fazer"

    return f"""
<article class="item-card{done_class} reveal" data-type="{esc(item["type_slug"])}" data-tags="{esc(" ".join(item["tag_slugs"]))}" data-search="{esc(item["search"])}" data-done="{str(item["done"]).lower()}" style="--reveal-delay: {delay}ms">
  <div class="item-head">
    <span class="item-check{checked_class}" aria-hidden="true">{CHECK_ICON}</span>
    <span class="item-id">{esc(item["id"])}</span>
    <h3 class="item-title">{esc(item["name"])}</h3>
  </div>
  <div class="item-body">
    <div class="item-meta">
      <span class="badge badge-type">{esc(item["tipo"])}</span>
      <span class="badge badge-priority priority-{item["priority_slug"]}"><span class="dot" aria-hidden="true"></span>{esc(item["prioridade"])}</span>
      {deadline_html}
    </div>
    {tags_block}
    {notes_block}
    {render_links(item)}
  </div>
  <span class="sr-only">{status}</span>
</article>"""


def render_lane(lane_key: str, items: list[dict], start_index: int) -> str:
    meta = LANES[lane_key]
    total = len(items)
    completed = sum(1 for item in items if item["done"])
    percent = round((completed / total) * 100, 2) if total else 0
    cards = "\n".join(render_card(item, start_index + index) for index, item in enumerate(items))
    empty_hidden = " hidden" if total else ""

    return f"""
<section class="lane {meta["class"]}" id="{lane_key.lower()}" data-lane="{lane_key.lower()}">
  <span class="lane-node" aria-hidden="true"></span>
  <header class="lane-header">
    <div class="lane-heading">
      <p class="lane-eyebrow">{esc(meta["label"])}</p>
      <h2>{lane_key}</h2>
    </div>
    <div class="lane-progress" aria-label="{completed} de {total} concluídos">
      <span class="lane-count">{completed} de {total}</span>
      <div class="lane-bar" aria-hidden="true"><span style="width: {percent:.2f}%"></span></div>
    </div>
  </header>
  <div class="lane-items">
    {cards}
  </div>
  <p class="lane-empty"{empty_hidden}>Nenhum item nesta raia com os filtros atuais.</p>
</section>"""


def render_lanes(plan: dict) -> str:
    parts: list[str] = []
    index = 0
    for lane_key in LANES:
        parts.append(render_lane(lane_key, plan["lanes"][lane_key], index))
        index += len(plan["lanes"][lane_key])
    return "\n".join(parts)


def build() -> tuple[dict, int, int]:
    plan = parse_plan(read_plan_text())
    front = plan["front"]
    items = [item for lane in LANES for item in plan["lanes"][lane]]
    total = len(items)
    completed = sum(1 for item in items if item["done"])
    percent = round((completed / total) * 100) if total else 0
    circumference = 2 * math.pi * 52
    offset = circumference * (1 - (completed / total if total else 0))
    updated_br = date.fromisoformat(front["atualizado"]).strftime("%d/%m/%Y")
    total_label = "1 item" if total == 1 else f"{total} itens"

    replacements = {
        "{{TITLE}}": esc(f'{front["titulo"]} · {front["nome"]}'),
        "{{DESCRIPTION}}": esc(front["resumo"]),
        "{{NAME}}": esc(front["nome"]),
        "{{ROLE}}": esc(front["cargo"]),
        "{{SUMMARY}}": esc(front["resumo"]),
        "{{UPDATED_BR}}": esc(updated_br),
        "{{UPDATED_ISO}}": esc(front["atualizado"]),
        "{{EDIT_URL}}": esc(EDIT_URL),
        "{{REPO_URL}}": esc(REPO_URL),
        "{{PAGE_URL}}": esc(PAGE_URL),
        "{{TOTAL}}": str(total),
        "{{TOTAL_LABEL}}": total_label,
        "{{COMPLETED}}": str(completed),
        "{{PERCENT}}": str(percent),
        "{{RING_CIRCUMFERENCE}}": f"{circumference:.4f}",
        "{{RING_OFFSET}}": f"{offset:.4f}",
        "{{TYPE_FILTERS}}": render_type_filters(items),
        "{{TAG_FILTERS}}": render_tag_filters(items),
        "{{LANES}}": render_lanes(plan),
    }

    template = (SRC / "template.html").read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace(key, value)

    leftovers = sorted(set(re.findall(r"\{\{[^}]+\}\}", template)))
    if leftovers:
        raise PlanError(f"Placeholders não substituídos: {', '.join(leftovers)}")

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "index.html").write_text(template, encoding="utf-8")
    shutil.copy2(SRC / "styles.css", DIST / "styles.css")
    shutil.copy2(SRC / "app.js", DIST / "app.js")
    shutil.copy2(SRC / "favicon.svg", DIST / "favicon.svg")
    return plan, total, completed


def main() -> int:
    try:
        _, total, completed = build()
    except PlanError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(f"Site gerado em dist/ · {completed}/{total} concluídos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
