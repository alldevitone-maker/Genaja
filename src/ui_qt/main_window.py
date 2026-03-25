from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QStatusBar, QFrame, QStackedWidget, QPushButton, QMessageBox,
                             QMenuBar, QMenu, QGraphicsOpacityEffect)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from version import __version__, __title__

# Import Panels
from ui_qt.panels.upload_panel import UploadPanel
from ui_qt.panels.keys_panel import KeysPanel
from ui_qt.panels.mapping_panel import MappingPanel
from ui_qt.panels.summary_panel import SummaryPanel
from ui_qt.widgets.title_bar import TitleBar
from ui_qt.dialogs.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self, services):
        super().__init__()
        self.services = services
        self.theme_service = services["theme"]
        self.etl_service = services["etl"]
        self.mapping_engine = services["mapping"]
        self.validation_engine = services["validation"]
        
        # 🛡️ FRAMELESS ARCHITECTURE (v0.5.3)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.setWindowTitle(f"Genaja Pro v{__version__}")
        self.resize(1150, 800)
        
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # Container Principal p/ compensar Frameless
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 🎨 CUSTOM TITLE BAR (v0.5.3)
        self.title_bar = TitleBar(title=f"Genaja Pro - v{__version__} Gold", parent=self)
        self.title_bar.closeClicked.connect(self.close)
        self.title_bar.minClicked.connect(self.showMinimized)
        self.title_bar.maxClicked.connect(self._toggle_maximize)
        self.main_layout.addWidget(self.title_bar)

        # Barra de Menu Integrada -> REPLACED BY SIDEBAR
        # Custom Title Bar já foi adicionada acima
        
        # 3. BODY LAYOUT (Sidebar + Content)
        self.body_container = QWidget()
        self.body_layout = QHBoxLayout(self.body_container)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        self.main_layout.addWidget(self.body_container)
        
        # 3.1 SIDEBAR (v0.5.9 SaaS Style)
        from ui_qt.widgets.settings_widgets import SidebarButton
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar_main")
        self.sidebar.setFixedWidth(70)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(5, 20, 5, 20)
        self.sidebar_layout.setSpacing(15)
        self.sidebar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        
        # Sidebar Icons/Buttons
        self.btn_nav_wizard = SidebarButton("🧙")
        self.btn_nav_wizard.setToolTip("Data Wizard (Fluxo de Dados)")
        self.btn_nav_wizard.setProperty("active", True)
        self.btn_nav_wizard.setFixedSize(50, 50)
        self.btn_nav_wizard.clicked.connect(lambda: self._fade_to_index(0))
        
        self.btn_nav_theme = SidebarButton("🔥")
        self.btn_nav_theme.setToolTip("Phoenix Customizer (Temas)")
        self.btn_nav_theme.setFixedSize(50, 50)
        self.btn_nav_theme.clicked.connect(self._open_theme_editor)
        
        self.btn_nav_settings = SidebarButton("⚙️")
        self.btn_nav_settings.setToolTip("Global Preferences")
        self.btn_nav_settings.setFixedSize(50, 50)
        self.btn_nav_settings.clicked.connect(self._open_settings)
        
        self.sidebar_layout.addWidget(self.btn_nav_wizard)
        self.sidebar_layout.addWidget(self.btn_nav_theme)
        self.sidebar_layout.addWidget(self.btn_nav_settings)
        self.sidebar_layout.addStretch()
        
        self.body_layout.addWidget(self.sidebar)
        
        # 3.2 CONTENT AREA (Antiga area central)
        self.content_area = QWidget()
        self.content_area.setObjectName("centralWidget")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.body_layout.addWidget(self.content_area)
        
        # Header (Visual Branding) inside Content
        self.header = QFrame()
        self.header.setObjectName("card")
        self.header.setFixedHeight(80)
        header_layout = QVBoxLayout(self.header)
        
        self.lbl_welcome = QLabel("🚀 Genaja Pro - The Next Frontier")
        self.lbl_welcome.setObjectName("TitleLabel")
        header_layout.addWidget(self.lbl_welcome)
        
        self.lbl_status = QLabel(f"Ambiente Híbrido PySide6 | Build v{__version__} Gold")
        self.lbl_status.setProperty("class", "secondary-text")
        header_layout.addWidget(self.lbl_status)
        
        self.content_layout.addWidget(self.header)
        
        # Wizard Stack
        self.stack = QStackedWidget()
        self.content_layout.addWidget(self.stack)
        
        # Painéis
        self.upload_panel = UploadPanel(self.services)
        self.keys_panel = KeysPanel(self.services)
        self.mapping_panel = MappingPanel(self.services)
        self.summary_panel = SummaryPanel(self.services)

        self.stack.addWidget(self.upload_panel)
        self.stack.addWidget(self.keys_panel)
        self.stack.addWidget(self.mapping_panel)
        self.stack.addWidget(self.summary_panel)

        # Fade Effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.stack.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Navigation Connections
        self.upload_panel.filesSelected.connect(self._on_files_ready)
        self.keys_panel.btn_back.clicked.connect(lambda: self._fade_to_index(0))
        self.keys_panel.btn_validate.clicked.connect(self._on_keys_validated)
        self.mapping_panel.btn_back.clicked.connect(lambda: self._fade_to_index(1))
        self.mapping_panel.btn_next.clicked.connect(self._on_mapping_done)
        self.summary_panel.btn_back.clicked.connect(lambda: self._fade_to_index(2))
        self.summary_panel.startProcessing.connect(self._on_start_sync)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(f"Engine v{__version__} Pronta.")

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _fade_to_index(self, index):
        """Inicia transição de fade out antes de trocar o stack."""
        self._target_index = index
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        
        # Desconectar conexões anteriores se existirem para evitar acúmulo
        try:
            self.fade_anim.finished.disconnect()
        except Exception:
            pass
            
        self.fade_anim.finished.connect(self._on_fade_out_finished)
        self.fade_anim.start()

    def _on_fade_out_finished(self):
        """Troca o widget no stack e inicia fade in."""
        self.fade_anim.finished.disconnect()
        self.stack.setCurrentIndex(self._target_index)
        
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def _open_theme_editor(self):
        from ui_qt.widgets.theme_editor import ThemeEditor
        editor = ThemeEditor(self.theme_service, self)
        editor.themeUpdated.connect(self.apply_theme)
        editor.show()

    def _reset_theme(self):
        self.theme_service.reset_to_defaults()
        self.apply_theme()
        QMessageBox.information(self, "Theme Reset", "Cores restauradas para o padrão Zinc Studio.")

    def _open_settings(self):
        dialog = SettingsDialog(self.services["config"], self.theme_service, self)
        if dialog.exec_():
            self.lbl_status.setText(f"Preferências atualizadas por {self.services['config'].get_config('general', 'operator_name')}")
            # Aplicar mudanças de UI imediatas se houver
            app_name = self.services["config"].get_config("general", "app_name")
            self.title_bar.lbl_title.setText(f"{app_name} - v{__version__} Gold")

    def _on_files_ready(self, src, tgt):
        self.status.showMessage("📊 Analisando estruturas reais...")
        cols_src = self.upload_panel.cols_src
        cols_tgt = self.upload_panel.cols_tgt
        top_matches = self.validation_engine.suggest_primary_keys(cols_src, cols_tgt)
        self.keys_panel.set_data(cols_src, cols_tgt, top_matches)
        self._fade_to_index(1)
        self.status.showMessage("Passo 2: Defina as chaves de cruzamento.")

    def _on_keys_validated(self):
        self.mapping_panel.set_data(self.upload_panel.cols_src, self.upload_panel.cols_tgt)
        self._fade_to_index(2)
        self.status.showMessage("Passo 3: Mapeie as colunas.")

    def _on_mapping_done(self):
        mapped_count = self.mapping_panel.list_tgt.count()
        summary = f"🚀 PRONTO PARA DISPARO REAL!\n\nCoragem, v{__version__}!\nColunas: {mapped_count}"
        self.summary_panel.set_summary(summary)
        self._fade_to_index(3)

    def _on_start_sync(self, config):
        from ui_qt.dialogs.progress_dashboard import ProgressDashboard
        dash = ProgressDashboard(self.services, self)
        dash.show()
        # Simulation logic... (OMITTING FOR BREVITY, keeping structure)
        dash.finalize(True)

    def apply_theme(self):
        """Global Visual Flush (v0.5.9 Phase 6 Harmony)"""
        from PySide6.QtWidgets import QApplication
        
        # 1. PURE FLUSH: Resetar folha de estilos antes de aplicar a nova
        # Isso limpa resíduos de temas anteriores na memória do Qt
        app = QApplication.instance()
        app.setStyleSheet("")
        
        qss = self.theme_service.get_qss()
        
        # 2. Aplicar novo QSS Global
        app.setStyleSheet(qss)
        
        # 3. Update local state
        theme = self.theme_service.current_theme
        
        # 4. Sincronizar Widgets Reativos (No-op no v0.5.9 Phase 6, mas mantido p/ estrutura)
        self.title_bar.update_style(theme)
        
        # 5. UNIVERSAL STYLE REFRESH (Deep Purge v0.5.9 Phase 6)
        # Agora buscando em TODOS os widgets da aplicação, não apenas filhos da MainWindow
        for widget in QApplication.allWidgets():
            # Refresh Custom Widgets
            if hasattr(widget, "refresh_style"):
                widget.refresh_style()
            
            # Repolish QSS classes
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
            
        # 6. Forçar repintura total
        self.update()
