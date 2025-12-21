"""Process page that lists available video recordings."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

try:
    from PySide6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QScrollArea,
        QGridLayout,
        QFrame,
        QLabel,
        QSizePolicy,
    )
    from PySide6.QtCore import Qt, QTimer
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QWidget,
            QVBoxLayout,
            QScrollArea,
            QGridLayout,
            QFrame,
            QLabel,
            QSizePolicy,
        )
        from PyQt6.QtCore import Qt, QTimer
    except ImportError:
        from PyQt5.QtWidgets import (
            QWidget,
            QVBoxLayout,
            QScrollArea,
            QGridLayout,
            QFrame,
            QLabel,
            QSizePolicy,
        )
        from PyQt5.QtCore import Qt, QTimer

from engine.detectors.game_detector import detect_game_from_video as detect_game
from gui.styles import theme
from registry.media_registry import is_registered
from utils import constants

LOGO_DIR = Path(__file__).resolve().parent.parent / "styles" / "logos"

class ProcessPage(QWidget):
    """Page that scans recording folders and displays video files."""

    def __init__(
        self,
        parent: QWidget | None = None,
        search_paths: Sequence[Path | str] | None = None,
        grid_columns: int = 6,
    ) -> None:
        super().__init__(parent)
        self.search_paths = [Path(p) for p in (search_paths or self._default_paths())]
        self.grid_columns = grid_columns
        self.allowed_ext = {".mp4", ".mov", ".mkv", ".avi"}
        self.tile_width = 220
        self.tile_height = 120
        self.grid_spacing = 30
        self._files_iter: Iterable[Path] | None = None
        self._build_ui()

    def _default_paths(self) -> list[Path]:
        return [Path(constants.MEDIA_DIR)]

    def _build_ui(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 16)
        layout.setSpacing(12)

        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(48)
        top_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(top_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.grid_host = QWidget()
        self.grid_layout = QGridLayout(self.grid_host)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(self.grid_spacing)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.grid_host.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.scroll_area.setWidget(self.grid_host)
        layout.addWidget(self.scroll_area)
        self._update_grid_margins()

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {theme.CANVAS_BG};
            }}
            QFrame#topBar {{
                background-color: {theme.CANVAS_BG};
                border-radius: 8px;
            }}
            QFrame#videoTile {{
                background-color: {theme.SIDEBAR_BUTTON_BG};
                border-radius: 10px;
                border: 1px solid #1c2029;
            }}
            QLabel#fileName {{
                color: {theme.SIDEBAR_TEXT};
                font-weight: 600;
                background: transparent;
            }}
            QLabel#fileMeta {{
                color: #b8c1cc;
                font-size: 12px;
                background: transparent;
            }}
            """
        )

    def refresh(self) -> None:
        files = self._scan_video_files(self.search_paths)
        self._clear_grid()
        self._files_iter = iter(files)
        QTimer.singleShot(0, self._process_next_file)

    def _scan_video_files(self, roots: Iterable[Path]) -> list[Path]:
        found: list[Path] = []
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in self.allowed_ext:
                    found.append(path)
        return sorted(found)

    def _clear_grid(self) -> None:
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _process_next_file(self) -> None:
        if self._files_iter is None:
            return
        for file_path in self._files_iter:
            if is_registered(str(file_path)):
                continue
            detected, game_name = detect_game(str(file_path))
            if detected and game_name:
                self._add_tile(file_path, game_name)
            break
        else:
            return

        self._update_grid_margins()
        QTimer.singleShot(0, self._process_next_file)

    def _add_tile(self, file_path: Path, game_name: str) -> None:
        tile = self._build_tile(file_path, game_name)
        idx = self.grid_layout.count()
        row = idx // self.grid_columns
        col = idx % self.grid_columns
        self.grid_layout.addWidget(tile, row, col)

    def _build_tile(self, file_path: Path, game_name: str) -> QFrame:
        tile = QFrame()
        tile.setObjectName("videoTile")
        tile.setFixedSize(self.tile_width, self.tile_height)
        self._apply_logo_background(tile, game_name)

        layout = QVBoxLayout(tile)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        name_label = QLabel(file_path.name)
        name_label.setObjectName("fileName")
        name_label.setWordWrap(False)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        name_label.setMinimumWidth(self.tile_width - 24)

        layout.addStretch(1)
        layout.addWidget(name_label)

        return tile

    def _apply_logo_background(self, tile: QFrame, game_name: str) -> None:
        logo_path = self._find_logo(game_name)
        if logo_path:
            tile.setStyleSheet(
                f"""
                QFrame#videoTile {{
                    background: {theme.SIDEBAR_BUTTON_BG};
                    border-radius: 10px;
                    border: 1px solid #1c2029;
                    background-image: url("{logo_path.as_posix()}");
                    background-position: center;
                    background-repeat: no-repeat;
                    background-size: cover;
                }}
                """
            )

    def _find_logo(self, game_name: str) -> Path | None:
        base = f"logo_{game_name}"
        for ext in (".png", ".jpg", ".jpeg", ".svg"):
            candidate = LOGO_DIR / f"{base}{ext}"
            if candidate.exists():
                return candidate
        return None

    def _update_grid_margins(self) -> None:
        if not self.scroll_area:
            return
        viewport_width = self.scroll_area.viewport().width()
        content_width = self.grid_columns * self.tile_width + (self.grid_columns - 1) * self.grid_spacing
        margin = max(0, (viewport_width - content_width) // 2)
        self.grid_layout.setContentsMargins(margin, 0, margin, 0)

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self._update_grid_margins()
