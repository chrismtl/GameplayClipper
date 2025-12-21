"""Main window composition and layout."""

from __future__ import annotations

from pathlib import Path

try:
    from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
    from PySide6.QtGui import QIcon
except ImportError:
    try:
        from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
        from PyQt6.QtGui import QIcon
    except ImportError:
        from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
        from PyQt5.QtGui import QIcon

from gui.navigation.sidebar import SidebarPanel
from gui.pages.home import HomePage
from gui.pages.process import ProcessPage


class MainWindow(QMainWindow):
    """Top-level window wiring sidebar and main content."""

    def __init__(self, app_icon: Path | None = None, title: str = "Tala Games") -> None:
        super().__init__()
        if app_icon and app_icon.is_file():
            self.setWindowIcon(QIcon(str(app_icon)))
        self.setWindowTitle(title)
        self.resize(1600, 900)
        self._build_layout()

    def _build_layout(self) -> None:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = SidebarPanel()
        layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.home_page = HomePage()
        self.process_page = ProcessPage()

        self.home_page.processRequested.connect(self.show_process_page)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.process_page)
        layout.addWidget(self.stack, 1)

        self.setCentralWidget(container)

    def show_process_page(self) -> None:
        self.process_page.refresh()
        self.stack.setCurrentWidget(self.process_page)
