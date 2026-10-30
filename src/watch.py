#!/usr/bin/env python3
"""Preview local com rebuild automático ao salvar plan.md ou arquivos de src/."""

from __future__ import annotations

import functools
import http.server
import os
import sys
import time
from pathlib import Path

import build

WATCHED = (
    build.PLAN,
    build.SRC / "template.html",
    build.SRC / "styles.css",
    build.SRC / "app.js",
    build.SRC / "favicon.svg",
)


def snapshot() -> dict[str, int | None]:
    return {
        str(path): path.stat().st_mtime_ns if path.exists() else None
        for path in WATCHED
    }


def rebuild() -> None:
    try:
        _, total, completed = build.build()
        print(f"Rebuild OK · {completed}/{total} concluídos")
    except build.PlanError as exc:
        print(f"Erro no build: {exc}", file=sys.stderr)


def main() -> int:
    rebuild()
    port = int(os.environ.get("PORT", "8000"))
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(build.DIST)
    )
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError as exc:
        print(
            f"Erro: não foi possível abrir a porta {port} ({exc}). "
            "Tente PORT=8001 make run.",
            file=sys.stderr,
        )
        return 1
    server.timeout = 0.5
    print(f"Preview em http://127.0.0.1:{port} (Ctrl+C para parar)")
    last = snapshot()
    try:
        while True:
            server.handle_request()
            current = snapshot()
            if current != last:
                last = current
                time.sleep(0.1)
                rebuild()
    except KeyboardInterrupt:
        print("\nParando preview.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
