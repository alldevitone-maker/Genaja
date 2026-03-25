from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QFrame, QLineEdit
from PySide6.QtCore import Qt, Signal

class MappingPanel(QWidget):
    finished = Signal(list) # Retorna as colunas mapeadas

    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        title_lbl = QLabel("⚙️ Passo 3: Mapeamento Comercial de Colunas")
        title_lbl.setObjectName("TitleLabel")
        self.layout.addWidget(title_lbl)
        
        # HUD Area (Search & Auto-Map)
        hud_layout = QHBoxLayout()
        self.search_ent = QLineEdit()
        self.search_ent.setPlaceholderText("🔍 Busca preditiva de colunas...")
        self.search_ent.textChanged.connect(self._filter_lists)
        hud_layout.addWidget(self.search_ent)
        
        self.btn_auto = QPushButton("🪄 Auto-Map I.A")
        self.btn_auto.setProperty("class", "primary-btn")
        hud_layout.addWidget(self.btn_auto)
        self.layout.addLayout(hud_layout)
        
        # Mapping Area (Dual List)
        lists_layout = QHBoxLayout()
        
        # Left: Available
        vbox_left = QVBoxLayout()
        vbox_left.addWidget(QLabel("Colunas Disponíveis (Origem):"))
        self.list_src = QListWidget()
        self.list_src.setSelectionMode(QListWidget.ExtendedSelection)
        vbox_left.addWidget(self.list_src)
        lists_layout.addLayout(vbox_left)
        
        # Center: Buttons
        vbox_mid = QVBoxLayout()
        vbox_mid.addStretch()
        self.btn_move_all = QPushButton("⏩")
        self.btn_move_sel = QPushButton("▶️")
        self.btn_back_sel = QPushButton("◀️")
        self.btn_back_all = QPushButton("⏪")
        
        vbox_mid.addWidget(self.btn_move_all)
        vbox_mid.addWidget(self.btn_move_sel)
        vbox_mid.addWidget(self.btn_back_sel)
        vbox_mid.addWidget(self.btn_back_all)
        vbox_mid.addStretch()
        lists_layout.addLayout(vbox_mid)
        
        # Right: Synced
        vbox_right = QVBoxLayout()
        vbox_right.addWidget(QLabel("A Sincronizar (Destino Final):"))
        self.list_tgt = QListWidget()
        self.list_tgt.setSelectionMode(QListWidget.ExtendedSelection)
        vbox_right.addWidget(self.list_tgt)
        lists_layout.addLayout(vbox_right)
        
        self.layout.addLayout(lists_layout)
        
        # Footer
        footer = QHBoxLayout()
        self.btn_back = QPushButton("⬅️ Voltar")
        self.btn_next = QPushButton("🚀 Configurar Regras Finais ➡️")
        self.btn_next.setProperty("class", "success-btn")
        
        footer.addWidget(self.btn_back)
        footer.addStretch()
        footer.addWidget(self.btn_next)
        self.layout.addLayout(footer)
        
        # Connections
        self.btn_move_sel.clicked.connect(self._move_selected_to_tgt)
        self.btn_back_sel.clicked.connect(self._move_selected_to_src)
        self.btn_move_all.clicked.connect(self._move_all_to_tgt)
        self.btn_back_all.clicked.connect(self._move_all_to_src)
        self.btn_auto.clicked.connect(self._on_auto_map)

    def set_data(self, cols_src, cols_tgt):
        self.full_list_src = cols_src
        self.full_list_tgt = cols_tgt
        self._filter_lists()

    def _on_auto_map(self):
        # Chamada ao MappingEngine Real
        engine = self.services.get("mapping")
        if engine:
            matches = engine.suggest_mapping(self.full_list_src, self.full_list_tgt)
            # matches é um dict {col_src: col_tgt}
            # Para o v0.5.0-alpha.3 simples, vamos apenas mover as colunas sugeridas para a direita
            cols_to_sync = list(matches.keys())
            
            self._move_all_to_src() # Reset
            
            for c in cols_to_sync:
                if c in self.full_list_src:
                    self.list_tgt.addItem(c)
            
            self._filter_lists()

    def _filter_lists(self):
        query = self.search_ent.text().lower()
        currently_in_tgt = [self.list_tgt.item(i).text() for i in range(self.list_tgt.count())]
        
        self.list_src.clear()
        for c in self.full_list_src:
            if c not in currently_in_tgt and query in c.lower():
                self.list_src.addItem(c)

    def _move_selected_to_tgt(self):
        for item in self.list_src.selectedItems():
            self.list_tgt.addItem(item.text())
            self.list_src.takeItem(self.list_src.row(item))
            
    def _move_selected_to_src(self):
        for item in self.list_tgt.selectedItems():
            self.list_src.addItem(item.text())
            self.list_tgt.takeItem(self.list_tgt.row(item))

    def _move_all_to_tgt(self):
        while self.list_src.count() > 0:
            item = self.list_src.takeItem(0)
            self.list_tgt.addItem(item.text())
            
    def _move_all_to_src(self):
        while self.list_tgt.count() > 0:
            item = self.list_tgt.takeItem(0)
            self.list_src.addItem(item.text())
