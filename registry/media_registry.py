"""Helpers to read/write media registry metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

REGISTRY_PATH = Path(__file__).with_name("registry.json")


def _load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # If corrupted or unreadable, start fresh
        return {}


def _save_registry(registry: Dict[str, Any]) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def register(filepath: str, game_detected: bool, gamename: str, first_frame: Any) -> None:
    """
    Add or overwrite a registry entry.

    Args:
        filepath: Absolute or relative path to the media file (used as key).
        game_detected: Internal game id detected.
        gamename: Human-friendly game name.
        first_frame: First frame reference/metadata.
    """
    registry = _load_registry()
    registry[str(filepath)] = {"gdetect": game_detected, "gname": gamename, "ff": first_frame}
    _save_registry(registry)


def is_registered(filename: str) -> bool:
    """
    Check whether a file is already registered.

    Args:
        filename: The key to look up (typically the file path string).
    """
    registry = _load_registry()
    return str(filename) in registry
