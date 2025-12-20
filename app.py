"""Application entry point wiring the GUI."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow


ICON_PATH = Path(__file__).parent / "gui" / "app_icon.png"
APP_NAME = "Tala Games"


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow(app_icon=ICON_PATH, title=APP_NAME)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
