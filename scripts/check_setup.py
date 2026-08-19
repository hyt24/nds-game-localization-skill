#!/usr/bin/env python3
"""Report configured localization capabilities without exposing secrets."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
from pathlib import Path


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def command_available(value: str) -> bool:
    if not value:
        return False
    executable = value.split()[0]
    return Path(executable).exists() or shutil.which(executable) is not None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, default=Path(".env"))
    args = parser.parse_args()
    load_env(args.env)
    mode = os.getenv("NDS_LOCALIZATION_MODE", "manual").lower()
    report = {
        "mode": mode,
        "python_modules": {
            "ndspy": importlib.util.find_spec("ndspy") is not None,
            "PIL": importlib.util.find_spec("PIL") is not None,
            "manga_ocr": importlib.util.find_spec("manga_ocr") is not None,
        },
        "local_ocr": {
            "vision_command": command_available(os.getenv("VISION_OCR_COMMAND", "")),
            "manga_command": command_available(os.getenv("MANGA_OCR_COMMAND", "")),
            "manga_model_configured": bool(os.getenv("MANGA_OCR_MODEL")),
        },
        "translation_api": {
            "provider_configured": bool(os.getenv("TRANSLATION_PROVIDER")),
            "model_configured": bool(os.getenv("TRANSLATION_MODEL")),
            "key_configured": bool(os.getenv("TRANSLATION_API_KEY")),
        },
        "vision_api": {
            "provider_configured": bool(os.getenv("VISION_PROVIDER")),
            "model_configured": bool(os.getenv("VISION_MODEL")),
            "key_configured": bool(os.getenv("VISION_API_KEY")),
        },
    }
    warnings = []
    if mode not in {"manual", "local", "hybrid"}:
        warnings.append("NDS_LOCALIZATION_MODE must be manual, local, or hybrid")
    if mode == "local" and not (report["local_ocr"]["vision_command"] or report["local_ocr"]["manga_command"] or report["python_modules"]["manga_ocr"]):
        warnings.append("local mode selected but no local OCR was detected")
    if mode == "hybrid" and not report["translation_api"]["key_configured"]:
        warnings.append("hybrid mode selected but no translation API key is configured")
    report["warnings"] = warnings
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
