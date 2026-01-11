from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QFileDialog, QInputDialog, QMessageBox, QSpacerItem, QSizePolicy, QLineEdit)
from PySide6.QtCore import Qt, Signal, QSettings
import os

class StartScreen(QWidget):
    open_db_signal = Signal(str, str)
    create_db_signal = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.settings = QSettings("Keyflow", "KeyflowApp")
        self.last_vault = self.settings.value("last_vault", "")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        title = QLabel("Keyflow")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #007acc; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Gestor Seguro de Contraseñas")
        subtitle.setStyleSheet("font-size: 16px; color: #888888; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)


        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        if self.last_vault and os.path.exists(self.last_vault):
            vault_name = os.path.basename(self.last_vault)
            
            last_vault_container = QWidget()
            last_vault_layout = QVBoxLayout(last_vault_container)
            last_vault_layout.setSpacing(10)
            
            vault_label = QLabel(f"Última Bóveda: {vault_name}")
            vault_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #007acc;")
            vault_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            last_vault_layout.addWidget(vault_label)
            
            self.last_vault_password = QLineEdit()
            self.last_vault_password.setPlaceholderText("Contraseña Maestra")
            self.last_vault_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.last_vault_password.setMinimumHeight(40)
            self.last_vault_password.returnPressed.connect(self.open_last_vault)
            last_vault_layout.addWidget(self.last_vault_password)
            
            open_last_btn = QPushButton("🔓 Abrir Bóveda")
            open_last_btn.setMinimumHeight(50)
            open_last_btn.setProperty("class", "primary")
            open_last_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            open_last_btn.clicked.connect(self.open_last_vault)
            last_vault_layout.addWidget(open_last_btn)
            
            layout.addWidget(last_vault_container)
            layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.create_btn = QPushButton("✨ Crear Nueva Base de Datos")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.setProperty("class", "primary")
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.clicked.connect(self.create_db)
        layout.addWidget(self.create_btn)

        self.open_btn = QPushButton("📂 Abrir Base de Datos Existente")
        self.open_btn.setMinimumHeight(50)
        self.open_btn.setProperty("class", "secondary")
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.clicked.connect(self.open_db)
        layout.addWidget(self.open_btn)

        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_db(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Crear Nueva Base de Datos", "", "Bases de Datos KeePass (*.kdbx)")
        if filepath:
            if not filepath.endswith(".kdbx"):
                filepath += ".kdbx"
            
            pwd, ok = QInputDialog.getText(self, "Establecer Contraseña Maestra", "Ingrese Contraseña Maestra:", echo=QLineEdit.EchoMode.Password)
            if ok and pwd:
                confirm, ok2 = QInputDialog.getText(self, "Confirmar Contraseña", "Confirmar Contraseña Maestra:", echo=QLineEdit.EchoMode.Password)
                if ok2 and confirm == pwd:
                    self.create_db_signal.emit(filepath, pwd)
                elif ok2:
                     QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            elif ok:
                 QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía")

    def open_db(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Base de Datos", "", "Bases de Datos KeePass (*.kdbx)")
        if filepath:
            pwd, ok = QInputDialog.getText(self, "Ingresar Contraseña Maestra", "Contraseña Maestra:", echo=QLineEdit.EchoMode.Password)
            if ok:
                self.open_db_signal.emit(filepath, pwd)


    def open_last_vault(self):
        if hasattr(self, 'last_vault_password'):
            pwd = self.last_vault_password.text()
            if pwd:
                self.open_db_signal.emit(self.last_vault, pwd)
            else:
                QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía")
