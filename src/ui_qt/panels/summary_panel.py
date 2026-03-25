from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QCheckBox, QGroupBox
from PySide6.QtCore import Qt, Signal

class SummaryPanel(QWidget):
    startProcessing = Signal(dict) # Retorna os inputs finais para o motor

    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        title_lbl = QLabel("🔥 Passo 4: Resumo Final & Disparo do Motor")
        title_lbl.setObjectName("TitleLabel")
        self.layout.addWidget(title_lbl)
        
        # Summary Area
        self.summary_box = QFrame()
        self.summary_box.setObjectName("card")
        summary_layout = QVBoxLayout(self.summary_box)
        
        self.lbl_summary = QLabel("Aguardando configuração...")
        self.lbl_summary.setWordWrap(True)
        summary_layout.addWidget(self.lbl_summary)
        self.layout.addWidget(self.summary_box)
        
        # Business Rules Group
        self.rules_group = QGroupBox("🛡️ Higienização & Blindagem (Data Governance)")
        rules_layout = QVBoxLayout(self.rules_group)
        
        self.chk_zeros = QCheckBox("I.A Sync: Auto-filtrar linhas com valor Zero/Nulo")
        self.chk_trim = QCheckBox("Limpar espaços extras (Trim)")
        self.chk_upper = QCheckBox("Padronizar para MAIÚSCULAS (Upper)")
        self.chk_clean = QCheckBox("Limpar colunas órfãs na saída")
        
        rules_layout.addWidget(self.chk_zeros)
        rules_layout.addWidget(self.chk_trim)
        rules_layout.addWidget(self.chk_upper)
        rules_layout.addWidget(self.chk_clean)
        self.layout.addWidget(self.rules_group)
        
        # Action Area
        self.layout.addStretch()
        
        footer = QHBoxLayout()
        self.btn_back = QPushButton("⬅️ Voltar ao Mapeamento")
        self.btn_run = QPushButton("⚡ INICIAR SINCRONIZAÇÃO CORPORATIVA ⚡")
        self.btn_run.setMinimumHeight(60)
        self.btn_run.setProperty("class", "success-btn")
        
        footer.addWidget(self.btn_back)
        footer.addStretch()
        footer.addWidget(self.btn_run)
        self.layout.addLayout(footer)
        
        self.btn_run.clicked.connect(self._on_run)

    def set_summary(self, config_text):
        self.lbl_summary.setText(config_text)
        
    def _on_run(self):
        config = {
            "chk_zeros": self.chk_zeros.isChecked(),
            "chk_trim": self.chk_trim.isChecked(),
            "chk_upper": self.chk_upper.isChecked(),
            "clean_output": self.chk_clean.isChecked()
        }
        self.startProcessing.emit(config)
