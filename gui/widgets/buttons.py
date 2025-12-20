"""Reusable button factories."""

from __future__ import annotations

try:
    from PySide6.QtWidgets import QPushButton
except ImportError:
    try:
        from PyQt6.QtWidgets import QPushButton
    except ImportError:
        from PyQt5.QtWidgets import QPushButton

from gui.styles import theme


def primary_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setFixedHeight(64)
    btn.setMinimumWidth(220)
    btn.setStyleSheet(
        f"""
        QPushButton {{
            background-color: {theme.PRIMARY_BG};
            color: {theme.PRIMARY_TEXT};
            border: none;
            border-radius: 14px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {theme.PRIMARY_BG_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {theme.PRIMARY_BG_PRESSED};
        }}
        """
    )
    return btn
