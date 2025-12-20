"""Animated collapsible sidebar widget."""

from __future__ import annotations

try:
    from PySide6.QtWidgets import (
        QWidget,
        QPushButton,
        QVBoxLayout,
        QSizePolicy,
        QSpacerItem,
    )
    from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QWidget,
            QPushButton,
            QVBoxLayout,
            QSizePolicy,
            QSpacerItem,
        )
        from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
    except ImportError:
        from PyQt5.QtWidgets import (
            QWidget,
            QPushButton,
            QVBoxLayout,
            QSizePolicy,
            QSpacerItem,
        )
        from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt

from gui.styles import theme


class SidebarPanel(QWidget):
    """Left-aligned sidebar with animated expand/collapse."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.collapsed_width = 56
        self.expanded_width = 220
        self._expanded = False

        self.setMinimumWidth(self.collapsed_width)
        self.setMaximumWidth(self.collapsed_width)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.animation = QPropertyAnimation(self, b"minimumWidth", self)
        self.animation.setDuration(220)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.finished.connect(self._on_animation_finished)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        self.hamburger_btn = QPushButton("≡")
        self.hamburger_btn.setObjectName("hamburger")
        self.hamburger_btn.setFixedSize(40, 32)
        self.hamburger_btn.clicked.connect(self.expand)

        self.collapse_btn = QPushButton("❮")
        self.collapse_btn.setObjectName("collapse")
        self.collapse_btn.setFixedSize(40, 32)
        self.collapse_btn.clicked.connect(self.collapse)
        self.collapse_btn.hide()

        self.menu_container = QWidget()
        menu_layout = QVBoxLayout(self.menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(10)
        for label in ("Detect", "Extract", "Query", "Create"):
            btn = QPushButton(label)
            btn.setMinimumHeight(36)
            menu_layout.addWidget(btn)

        menu_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.menu_container.hide()

        layout.addWidget(self.hamburger_btn, alignment=Qt.AlignTop)
        layout.addWidget(self.collapse_btn, alignment=Qt.AlignTop)
        layout.addWidget(self.menu_container)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self._apply_style()

    def _apply_style(self) -> None:
        self.setObjectName("sidebar")
        self.setStyleSheet(
            f"""
            QWidget#sidebar {{
                background-color: {theme.SIDEBAR_BG};
            }}
            QPushButton {{
                background-color: {theme.SIDEBAR_BUTTON_BG};
                color: {theme.SIDEBAR_TEXT};
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {theme.SIDEBAR_BUTTON_BG_HOVER};
            }}
            QPushButton#hamburger, QPushButton#collapse {{
                font-size: 16px;
                text-align: center;
                padding: 0;
            }}
            """
        )

    def expand(self) -> None:
        if self._expanded:
            return
        self._expanded = True
        self.menu_container.hide()
        self.hamburger_btn.hide()
        self.collapse_btn.show()

        self.animation.stop()
        self.setMaximumWidth(self.expanded_width)
        self.animation.setStartValue(self.minimumWidth())
        self.animation.setEndValue(self.expanded_width)
        self.animation.start()

    def collapse(self) -> None:
        if not self._expanded:
            return
        self._expanded = False
        self.menu_container.hide()
        self.collapse_btn.hide()
        self.hamburger_btn.show()

        self.animation.stop()
        self.setMaximumWidth(self.expanded_width)
        self.animation.setStartValue(self.minimumWidth())
        self.animation.setEndValue(self.collapsed_width)
        self.animation.start()

    def _on_animation_finished(self) -> None:
        if self._expanded:
            self.setMinimumWidth(self.expanded_width)
            self.setMaximumWidth(self.expanded_width)
            self.menu_container.show()
        else:
            self.setMinimumWidth(self.collapsed_width)
            self.setMaximumWidth(self.collapsed_width)
