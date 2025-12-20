"""Home/landing page content."""

from __future__ import annotations

try:
    from PySide6.QtWidgets import QWidget, QVBoxLayout
    from PySide6.QtCore import Qt
except ImportError:
    try:
        from PyQt6.QtWidgets import QWidget, QVBoxLayout
        from PyQt6.QtCore import Qt
    except ImportError:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout
        from PyQt5.QtCore import Qt

from gui.styles import theme
from gui.widgets.buttons import primary_button


class HomePage(QWidget):
    """Landing page with primary action entry point."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)

        process_btn = primary_button("Process")
        layout.addWidget(process_btn, alignment=Qt.AlignCenter)

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {theme.CANVAS_BG};
            }}
            """
        )
