from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class TitleBar(QWidget):
    closeClicked = Signal()
    minClicked = Signal()
    maxClicked = Signal()

    def __init__(self, title="Genaja Pro", parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setObjectName("titleBar")
        self.setFixedHeight(32)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Icon
        self.icon_lbl = QLabel("🧬") # Placeholder for icon
        self.layout.addWidget(self.icon_lbl)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("titleLabel")
        self.layout.addWidget(self.title_lbl)
        
        self.layout.addStretch()
        
        # Buttons
        self.btn_min = QPushButton("－")
        self.btn_min.setObjectName("titleBarBtn")
        self.btn_min.setFixedSize(45, 32)
        self.btn_min.clicked.connect(self.minClicked.emit)
        
        self.btn_max = QPushButton("▢")
        self.btn_max.setObjectName("titleBarBtn")
        self.btn_max.setFixedSize(45, 32)
        self.btn_max.clicked.connect(self.maxClicked.emit)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("titleBarClose")
        self.btn_close.setFixedSize(45, 32)
        self.btn_close.clicked.connect(self.closeClicked.emit)
        
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPosition().toPoint()
            self._window_pos = self._parent.pos()

    def mouseMoveEvent(self, event):
        if hasattr(self, '_start_pos'):
            delta = event.globalPosition().toPoint() - self._start_pos
            self._parent.move(self._window_pos + delta)

    def update_style(self, theme):
        """No-op: Todo o estilo é controlado via QSS Global no v0.5.9 Phase 6."""
        pass
