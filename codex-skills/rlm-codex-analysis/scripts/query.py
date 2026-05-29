#!/usr/bin/env python3
"""Thin wrapper around the local rlm-codex CLI."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    cli = Path(os.environ.get("RLM_CODEX_CLI", "~/work/rlm-codex-cli/bin/rlm-codex")).expanduser()
    if not cli.exists():
        print(f"error: rlm-codex CLI not found at {cli}", file=sys.stderr)
        print("set RLM_CODEX_CLI to override the path", file=sys.stderr)
        return 1

    cmd = [str(cli), "query", *sys.argv[1:]]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
