from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QAbstractButton
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, Property, Signal, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

class ModernSwitch(QAbstractButton):
    def __init__(self, theme_service, parent=None, track_radius=12, thumb_radius=10):
        super().__init__(parent)
        self.theme_service = theme_service
        self.setCheckable(True)
        self.setFixedSize(48, 24)
        
        self._track_radius = track_radius
        self._thumb_radius = thumb_radius
        
        self._offset = self._thumb_radius + 2
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Colors (Dynamic from tokens)
        self._update_colors()

    def _update_colors(self):
        self._track_color_off = QColor(self.theme_service.get_color("border_col"))
        self._track_color_on = QColor(self.theme_service.get_color("action_bg"))
        self._thumb_color = QColor(self.theme_service.get_color("fg_col"))

    @Property(float)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def nextCheckState(self):
        super().nextCheckState()
        start = self._offset
        end = self.width() - self._thumb_radius - 2 if self.isChecked() else self._thumb_radius + 2
        
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Draw track
        curr_track_col = self._track_color_on if self.isChecked() else self._track_color_off
        p.setBrush(curr_track_col)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), self._track_radius, self._track_radius)
        
        # Draw thumb
        p.setBrush(self._thumb_color)
        p.drawEllipse(QRect(int(self._offset - self._thumb_radius), int(self.height()/2 - self._thumb_radius), 
                            int(self._thumb_radius * 2), int(self._thumb_radius * 2)))

class SettingCard(QFrame):
    def __init__(self, title, subtitle, control_widget, parent=None):
        super().__init__(parent)
        self.setObjectName("SettingCard")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        self.label_title = QLabel(title)
        self.label_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.label_desc = QLabel(subtitle)
        self.label_desc.setStyleSheet("color: #A1A1AA; font-size: 11px;")
        self.label_desc.setWordWrap(True)
        
        text_layout.addWidget(self.label_title)
        text_layout.addWidget(self.label_desc)
        
        layout.addWidget(text_container, 1)
        layout.addWidget(control_widget, 0)

class SidebarButton(QPushButton):
    # This will be styled via QSS using [active="true"]
    pass
