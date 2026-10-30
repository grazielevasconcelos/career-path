#!/usr/bin/env python3
"""Preview local com rebuild automático ao salvar career.md ou arquivos de src/."""

from __future__ import annotations

import functools
import http.server
import os
import signal
import sys
import time
from pathlib import Path

import build

WATCHED = (
    build.SOURCE,
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
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(build.DIST)
    )
    try:
        server = http.server.ThreadingHTTPServer((host, port), handler)
    except OSError as exc:
        print(
            f"Erro: não foi possível abrir {host}:{port} ({exc}). "
            "Tente PORT=8001 make run ou ajuste HOST/PORT.",
            file=sys.stderr,
        )
        return 1
    server.timeout = 0.5
    display_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    if ":" in display_host and not display_host.startswith("["):
        display_host = f"[{display_host}]"
    print(f"Preview em http://{display_host}:{port} (Ctrl+C para parar)")
    last = snapshot()
    stopping = False

    def request_stop(_signum: int, _frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    try:
        while not stopping:
            server.handle_request()
            current = snapshot()
            if current != last:
                last = current
                time.sleep(0.1)
                rebuild()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    print("\nParando preview.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
