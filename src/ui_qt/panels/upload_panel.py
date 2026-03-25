from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QFrame
from PySide6.QtCore import Qt, Signal

class DropZone(QFrame):
    clicked = Signal()
    fileDropped = Signal(str)

    def __init__(self, title, initial_msg):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        self.setCursor(Qt.PointingHandCursor)
        
        self.layout = QVBoxLayout(self)
        self.lbl_title = QLabel(title)
        self.lbl_title.setProperty("class", "action-text")
        self.layout.addWidget(self.lbl_title, alignment=Qt.AlignTop)
        
        self.lbl_msg = QLabel(initial_msg)
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setAlignment(Qt.AlignCenter)
        self.lbl_msg.setProperty("class", "secondary-text")
        self.layout.addWidget(self.lbl_msg, 1)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.setProperty("active", True)
            self.style().unpolish(self)
            self.style().polish(self)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setProperty("active", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("active", False)
        self.style().unpolish(self)
        self.style().polish(self)
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            excel_files = [f for f in files if f.endswith(('.xlsx', '.xls'))]
            if excel_files:
                self.fileDropped.emit(excel_files[0])
            else:
                self.lbl_msg.setText("❌ Apenas arquivos Excel!")
                self.lbl_msg.setProperty("class", "danger-text")

class UploadPanel(QWidget):
    filesSelected = Signal(str, str)

    def __init__(self, services, parent=None):
        super().__init__(parent)
        self.services = services
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(15)
        
        title_lbl = QLabel("📂 Passo 1: Seleção de Fontes de Dados")
        title_lbl.setObjectName("TitleLabel")
        self.layout.addWidget(title_lbl)
        
        zones_layout = QHBoxLayout()
        self.drop_src = DropZone("Planilha de ORIGEM", "Arraste o arquivo aqui\nou clique para buscar")
        self.drop_tgt = DropZone("Planilha de DESTINO", "Arraste o arquivo aqui\nou clique para buscar")
        
        zones_layout.addWidget(self.drop_src)
        zones_layout.addWidget(self.drop_tgt)
        self.layout.addLayout(zones_layout)
        
        self.path_src = ""
        self.path_tgt = ""
        
        self.drop_src.clicked.connect(lambda: self._ask_file("src"))
        self.drop_tgt.clicked.connect(lambda: self._ask_file("tgt"))
        self.drop_src.fileDropped.connect(lambda f: self._set_file("src", f))
        self.drop_tgt.fileDropped.connect(lambda f: self._set_file("tgt", f))
        
        self.btn_next = QPushButton("Próximo Passo (Mapeamento) ➡️")
        self.btn_next.setEnabled(False)
        self.btn_next.setMinimumHeight(45)
        self.btn_next.clicked.connect(self._on_next)
        self.layout.addWidget(self.btn_next, alignment=Qt.AlignRight)

    def _ask_file(self, mode):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Planilha", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self._set_file(mode, path)

    def _set_file(self, mode, path):
        short_name = path.replace('\\', '/').split('/')[-1]
        self.drop_src.setCursor(Qt.WaitCursor) if mode == "src" else self.drop_tgt.setCursor(Qt.WaitCursor)
        
        try:
            # No v0.5.0, usamos o motor real injetado
            # Precisamos de um logger_func (passamos print para o console por enquanto ou statusbar)
            from services.excel_loader import load_excel_data_with_adjustment
            
            # Nota: load_excel_data_with_adjustment espera (file, type, root, logger)
            # Para o Qt, o 'root' pode ser None ou o próprio widget
            df = load_excel_data_with_adjustment(path, mode.upper(), self, print)
            
            if df is not None:
                if mode == "src":
                    self.path_src = path
                    self.cols_src = list(df.columns)
                    self.drop_src.lbl_msg.setText(f"✅ ORIGEM CARREGADA:\n{short_name}\n({len(df)} linhas)")
                    self.drop_src.lbl_msg.setProperty("class", "success-text")
                    self.drop_src.lbl_msg.style().unpolish(self.drop_src.lbl_msg)
                    self.drop_src.lbl_msg.style().polish(self.drop_src.lbl_msg)
                else:
                    self.path_tgt = path
                    self.cols_tgt = list(df.columns)
                    self.drop_tgt.lbl_msg.setText(f"✅ DESTINO CARREGADO:\n{short_name}\n({len(df)} linhas)")
                    self.drop_tgt.lbl_msg.setProperty("class", "success-text")
                    self.drop_tgt.lbl_msg.style().unpolish(self.drop_tgt.lbl_msg)
                    self.drop_tgt.lbl_msg.style().polish(self.drop_tgt.lbl_msg)
            else:
                raise Exception("Falha na leitura do buffer Excel.")
                
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Erro de Leitura", f"Não foi possível processar o arquivo:\n{e}")
            if mode == "src": self.path_src = ""
            else: self.path_tgt = ""
        finally:
            self.drop_src.setCursor(Qt.PointingHandCursor)
            self.drop_tgt.setCursor(Qt.PointingHandCursor)
            
        if self.path_src and self.path_tgt:
            self.btn_next.setEnabled(True)

    def _on_next(self):
        # Emitimos os dados reais para a MainWindow
        data = {
            "path_src": self.path_src,
            "path_tgt": self.path_tgt,
            "cols_src": self.cols_src,
            "cols_tgt": self.cols_tgt
        }
        self.filesSelected.emit(self.path_src, self.path_tgt) # Mantendo assinatura antiga por compatibilidade de sinal
        # Mas podemos emitir um sinal extra ou acessar via MainWindow
