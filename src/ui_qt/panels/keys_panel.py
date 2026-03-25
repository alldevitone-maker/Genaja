from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QFrame
from PySide6.QtCore import Qt, Signal

class KeysPanel(QWidget):
    validated = Signal(dict) # Retorna as chaves selecionadas

    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        title_lbl = QLabel("🧠 Passo 2: Configuração de Chaves & Blindagem")
        title_lbl.setObjectName("TitleLabel")
        self.layout.addWidget(title_lbl)
        
        self.container = QFrame()
        self.container.setObjectName("card")
        self.inner_layout = QVBoxLayout(self.container)
        
        # Grid-like layout for keys
        keys_row = QHBoxLayout()
        
        # Col 1: Src Key
        src_vbox = QVBoxLayout()
        src_vbox.addWidget(QLabel("Chave na Origem:"))
        self.combo_src = QComboBox()
        src_vbox.addWidget(self.combo_src)
        keys_row.addLayout(src_vbox)
        
        keys_row.addWidget(QLabel("🔗"), alignment=Qt.AlignCenter)
        
        # Col 2: Tgt Key
        tgt_vbox = QVBoxLayout()
        tgt_vbox.addWidget(QLabel("Chave no Destino:"))
        self.combo_tgt = QComboBox()
        tgt_vbox.addWidget(self.combo_tgt)
        keys_row.addLayout(tgt_vbox)
        
        self.inner_layout.addLayout(keys_row)
        
        # Protected Key Area
        self.inner_layout.addWidget(QLabel("⭐ Configuração de Chave Protegida (A1)"))
        self.protected_row = QHBoxLayout()
        self.chk_protected = QCheckBox("Ativar Blindagem na Posição A1")
        self.protected_row.addWidget(self.chk_protected)
        
        self.combo_protected = QComboBox()
        self.combo_protected.setEnabled(False)
        self.protected_row.addWidget(self.combo_protected)
        self.inner_layout.addLayout(self.protected_row)
        
        self.chk_protected.toggled.connect(self.combo_protected.setEnabled)
        
        self.layout.addWidget(self.container)
        
        # Footer buttons
        footer = QHBoxLayout()
        self.btn_back = QPushButton("⬅️ Voltar")
        self.btn_validate = QPushButton("🔒 Validar e Prosseguir")
        self.btn_validate.setProperty("class", "success-btn")
        
        footer.addWidget(self.btn_back)
        footer.addStretch()
        footer.addWidget(self.btn_validate)
        self.layout.addLayout(footer)

    def set_data(self, cols_src, cols_tgt, top_matches=None):
        self.combo_src.clear()
        self.combo_tgt.clear()
        self.combo_protected.clear()
        
        self.combo_src.addItems(cols_src)
        self.combo_tgt.addItems(cols_tgt)
        self.combo_protected.addItems(cols_tgt)
        
        # Uso do ValidationEngine via top_matches
        if top_matches:
            # top_matches é uma tupla (best_src, best_tgt, score) ou o que o motor retornar
            # Se for a tupla padrão:
            if isinstance(top_matches, tuple) and len(top_matches) >= 2:
                src_key = top_matches[0]
                tgt_key = top_matches[1]
            # Caso seja uma lista de matches (estilo v0.4.9 legado ou futura expansão)
            elif isinstance(top_matches, list) and len(top_matches) > 0:
                best = top_matches[0]
                src_key = best.get('src') if isinstance(best, dict) else best[0]
                tgt_key = best.get('tgt') if isinstance(best, dict) else best[1]
            else:
                return # Formato desconhecido
            
            idx_s = self.combo_src.findText(src_key)
            idx_t = self.combo_tgt.findText(tgt_key)
            
            if idx_s >= 0: self.combo_src.setCurrentIndex(idx_s)
            if idx_t >= 0: self.combo_tgt.setCurrentIndex(idx_t)
            
        # Fallback se não houver match
        if self.combo_src.currentIndex() == -1:
            for i in range(self.combo_src.count()):
                if "ID" in self.combo_src.itemText(i).upper():
                    self.combo_src.setCurrentIndex(i)
                    break
