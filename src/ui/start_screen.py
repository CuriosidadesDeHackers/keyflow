from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QFileDialog, QInputDialog, QMessageBox, QSpacerItem, QSizePolicy, QLineEdit, QHBoxLayout,
                               QProgressBar, QApplication)
from PySide6.QtCore import Qt, Signal, QSettings
import os
from .password_dialog import MasterPasswordDialog, EnterPasswordDialog

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
            
            password_layout = QHBoxLayout()
            password_layout.setSpacing(10)

            self.last_vault_password = QLineEdit()
            self.last_vault_password.setPlaceholderText("Contraseña Maestra")
            self.last_vault_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.last_vault_password.setMinimumHeight(45)
            
            # Conectar cambio de texto para ajustar tamaño de fuente dinámicamente
            self.last_vault_password.textChanged.connect(self.update_password_style)
            # Estilo inicial (placeholder pequeño)
            self.last_vault_password.setStyleSheet("font-size: 14px; padding: 10px;")
            
            self.last_vault_password.returnPressed.connect(self.open_last_vault)
            password_layout.addWidget(self.last_vault_password)

            self.toggle_visibility_btn = QPushButton("👁️")
            self.toggle_visibility_btn.setMinimumHeight(45)
            self.toggle_visibility_btn.setFixedWidth(50)
            self.toggle_visibility_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.toggle_visibility_btn.clicked.connect(self.toggle_password_visibility)
            password_layout.addWidget(self.toggle_visibility_btn)

            last_vault_layout.addLayout(password_layout)
            
            # Barra de progreso (animación de carga)
            self.loading_bar = QProgressBar()
            self.loading_bar.setRange(0, 0) # Indeterminado (animación continua)
            self.loading_bar.setTextVisible(False)
            self.loading_bar.setFixedHeight(5)
            self.loading_bar.setVisible(False)
            self.loading_bar.setStyleSheet("QProgressBar { background-color: transparent; border: none; } QProgressBar::chunk { background-color: #007acc; }")
            last_vault_layout.addWidget(self.loading_bar)
            
            open_last_btn = QPushButton("Abrir Bóveda")
            open_last_btn.setMinimumHeight(50)
            open_last_btn.setProperty("class", "primary")
            open_last_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            open_last_btn.clicked.connect(self.open_last_vault)
            last_vault_layout.addWidget(open_last_btn)
            
            layout.addWidget(last_vault_container)
            layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.create_btn = QPushButton("Crear Nueva Base de Datos")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.setProperty("class", "primary")
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.clicked.connect(self.create_db)
        layout.addWidget(self.create_btn)

        self.open_btn = QPushButton("Abrir Base de Datos Existente")
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
            
            dialog = MasterPasswordDialog(self)
            if dialog.exec():
                pwd = dialog.get_password()
                self.create_db_signal.emit(filepath, pwd)

    def open_db(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Base de Datos", "", "Bases de Datos KeePass (*.kdbx)")
        if filepath:
            dialog = EnterPasswordDialog(self)
            if dialog.exec():
                pwd = dialog.get_password()
                self.open_db_signal.emit(filepath, pwd)


    def open_last_vault(self):
        if hasattr(self, 'last_vault_password'):
            pwd = self.last_vault_password.text()
            if pwd:
                # Mostrar animación de carga
                if hasattr(self, 'loading_bar'):
                    self.loading_bar.setVisible(True)
                
                self.last_vault_password.setEnabled(False)
                if hasattr(self, 'toggle_visibility_btn'):
                    self.toggle_visibility_btn.setEnabled(False)
                    
                # Forzar actualización de la UI para que se vea la animación antes del bloqueo
                QApplication.processEvents()
                
                try:
                    self.open_db_signal.emit(self.last_vault, pwd)
                finally:
                    # Restaurar estado si regresa el control (por error o loop)
                    if hasattr(self, 'loading_bar'):
                        self.loading_bar.setVisible(False)
                    self.last_vault_password.setEnabled(True)
                    if hasattr(self, 'toggle_visibility_btn'):
                        self.toggle_visibility_btn.setEnabled(True)
                    self.last_vault_password.setFocus()
            else:
                QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía")

    def toggle_password_visibility(self):
        if self.last_vault_password.echoMode() == QLineEdit.EchoMode.Password:
            self.last_vault_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_visibility_btn.setText("🔒")
        else:
            self.last_vault_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_visibility_btn.setText("👁️")

    def update_password_style(self, text):
        """Cambia el estilo del campo de contraseña según si tiene texto o no."""
        if text:
            # Si hay texto, hacer los asteriscos grandes
            self.last_vault_password.setStyleSheet("font-size: 24px; padding: 5px; letter-spacing: 2px;")
        else:
            # Si está vacío (placeholder visible), usar fuente normal
            self.last_vault_password.setStyleSheet("font-size: 14px; padding: 10px;")

    def showEvent(self, event):
        """Limpiar el campo de contraseña cada vez que se muestre la pantalla."""
        super().showEvent(event)
        if hasattr(self, 'last_vault_password'):
            self.last_vault_password.clear()
            self.last_vault_password.setEchoMode(QLineEdit.EchoMode.Password)
            if hasattr(self, 'toggle_visibility_btn'):
                self.toggle_visibility_btn.setText("👁️")
            self.last_vault_password.setFocus()
