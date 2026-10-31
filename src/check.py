#!/usr/bin/env python3
"""Valida o career.md e o site gerado em dist/ antes do deploy."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser

import build

REQUIRED_FILES = (
    "index.html",
    "styles.css",
    "app.js",
    "favicon.svg",
    "fonts/Inter-Variable.woff2",
)


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.scripts: list[str] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"] or "")
        if tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
            self.stylesheets.append(values["href"] or "")


def fail(message: str) -> int:
    print(f"Erro: {message}", file=sys.stderr)
    return 1


def extract_lane(html_text: str, lane_id: str) -> str | None:
    pattern = re.compile(
        rf'<section[^>]*class="[^"]*lane[^"]*"[^>]*id="{re.escape(lane_id)}"[\s\S]*?</section>',
        re.IGNORECASE,
    )
    match = pattern.search(html_text)
    return match.group(0) if match else None


def main() -> int:
    try:
        plan = build.parse_plan(build.read_plan_text())
    except build.PlanError as exc:
        return fail(str(exc))

    missing = [name for name in REQUIRED_FILES if not (build.DIST / name).exists()]
    if missing:
        return fail(f"Arquivos ausentes em dist/: {', '.join(missing)}. Rode 'make build'.")

    html_text = (build.DIST / "index.html").read_text(encoding="utf-8")
    if "{{" in html_text:
        return fail("O HTML gerado ainda contém placeholders não substituídos.")
    if 'lang="pt-BR"' not in html_text:
        return fail("O HTML gerado não declara lang=\"pt-BR\".")
    if 'data-theme="light"' not in html_text:
        return fail("O HTML gerado não define o tema claro como padrão.")

    parser = DocumentParser()
    parser.feed(html_text)
    for lane_key in build.LANES:
        lane_id = lane_key.lower()
        if lane_id not in parser.ids:
            return fail(f"Seção da raia ausente no HTML: #{lane_id}.")

    if "styles.css" not in parser.stylesheets:
        return fail("O HTML não referencia styles.css.")
    if "app.js" not in parser.scripts:
        return fail("O HTML não referencia app.js.")
    if "print-dialog" not in parser.ids:
        return fail("O guia de impressão não foi gerado no HTML.")

    css_text = (build.DIST / "styles.css").read_text(encoding="utf-8")
    if "@font-face" not in css_text:
        return fail("styles.css não declara a fonte Inter (@font-face).")
    if "@media print" not in css_text:
        return fail("styles.css não contém regras de impressão (@media print).")
    items = [item for lane in build.LANES for item in plan["lanes"][lane]]
    total = len(items)
    completed = sum(1 for item in items if item["done"])
    if total == 0:
        return fail("O plano não tem itens.")

    expected_progress = f"<strong>{completed}</strong> de {total} concluídos"
    if expected_progress not in html_text:
        return fail(f"Contador de progresso esperado não encontrado: {expected_progress}.")

    expected_total = "1 item" if total == 1 else f"{total} itens"
    if expected_total not in html_text:
        return fail(f"Contador total esperado não encontrado: {expected_total}.")

    for lane_key, lane_items in plan["lanes"].items():
        lane_id = lane_key.lower()
        section = extract_lane(html_text, lane_id)
        if section is None:
            return fail(f"Não foi possível isolar a seção #{lane_id} no HTML.")
        for item in lane_items:
            marker = f'<span class="item-id">{build.esc(item["id"])}</span>'
            if marker not in section:
                return fail(f"Item {item['id']} não está dentro da seção #{lane_id}.")
            title = f'<h3 class="item-title">{build.esc(item["name"])}</h3>'
            if title not in section:
                return fail(f"Título do item {item['id']} não aparece na seção #{lane_id}.")
            if item["link"] and build.esc(item["link"]) not in section:
                return fail(f"Link do item {item['id']} não aparece na seção #{lane_id}.")
            if item["done"] and "is-done" not in section:
                return fail(f"Item concluído {item['id']} não recebeu a classe is-done.")
            for slug in item["tag_slugs"]:
                if f'data-tag="{build.esc(slug)}"' not in html_text:
                    return fail(f"Filtro da tag '{slug}' não foi gerado.")

    types = []
    for item in items:
        if item["type_slug"] not in types:
            types.append(item["type_slug"])
    for type_slug in types:
        if f'data-type="{build.esc(type_slug)}"' not in html_text:
            return fail(f"Filtro do tipo '{type_slug}' não foi gerado.")

    if "stroke-dashoffset=" not in html_text:
        return fail("O anel de progresso não foi gerado.")
    if 'id="search"' not in html_text:
        return fail("O campo de busca não foi gerado.")
    if 'id="clear-filters"' not in html_text:
        return fail("O botão de limpar filtros não foi gerado.")

    for name in ("styles.css", "app.js", "favicon.svg", "fonts/Inter-Variable.woff2"):
        if (build.DIST / name).stat().st_size == 0:
            return fail(f"Arquivo vazio em dist/: {name}.")

    completed_label = "1 concluído" if completed == 1 else f"{completed} concluídos"
    print(
        f"OK: career.md válido · {total} itens · {completed_label} · "
        f"site pronto em dist/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
