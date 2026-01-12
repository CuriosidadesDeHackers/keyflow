from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt

class BasePasswordDialog(QDialog):
    def __init__(self, parent=None, title="Keyflow"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(420)
        self.setModal(True)
        # Remove help context button from title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

    def create_header(self, title_text, subtitle_text):
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #007acc; margin-bottom: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)
        
        subtitle = QLabel(subtitle_text)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 13px; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(subtitle)

    def create_styled_input(self, placeholder=""):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setEchoMode(QLineEdit.EchoMode.Password)
        inp.setMinimumHeight(45)
        # Estilo premium para el input de contraseña
        inp.setStyleSheet("""
            QLineEdit {
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: #252525;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
                background-color: #2d2d2d;
            }
        """)
        
        # Conectar cambio de texto para efecto de "escritura segura" (asteriscos grandes)
        inp.textChanged.connect(lambda text: self._update_input_style(inp, text))
        
        layout.addWidget(inp)
        
        toggle = QPushButton("👁️")
        toggle.setFixedSize(45, 45)
        toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border-color: #007acc;
            }
        """)
        
        # Toggle logic
        def toggle_visibility():
            if inp.echoMode() == QLineEdit.EchoMode.Password:
                inp.setEchoMode(QLineEdit.EchoMode.Normal)
                toggle.setText("🔒")
            else:
                inp.setEchoMode(QLineEdit.EchoMode.Password)
                toggle.setText("👁️")
                
        toggle.clicked.connect(toggle_visibility)
        layout.addWidget(toggle)
        
        return {'container': container, 'input': inp}

    def _update_input_style(self, widget, text):
        if text:
            # Texto presente: fuente más grande y espaciada para asteriscos
            widget.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #404040;
                    border-radius: 5px;
                    padding: 5px 10px;
                    font-size: 24px;
                    letter-spacing: 2px;
                    background-color: #252525;
                }
                QLineEdit:focus {
                    border: 1px solid #007acc;
                    background-color: #2d2d2d;
                }
            """)
        else:
            # Placeholder: fuente normal
            widget.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #404040;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                    background-color: #252525;
                }
                QLineEdit:focus {
                    border: 1px solid #007acc;
                    background-color: #2d2d2d;
                }
            """)

class MasterPasswordDialog(BasePasswordDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Crear Nueva Bóveda")
        
        self.create_header("Seguridad de la Bóveda", 
                         "Establece una contraseña maestra fuerte. Esta será la única llave para acceder a tus datos.")

        # Inputs
        self.layout.addWidget(QLabel("Contraseña Maestra:"))
        self.pwd_input = self.create_styled_input("Ingresa tu contraseña")
        self.layout.addWidget(self.pwd_input['container'])

        self.layout.addWidget(QLabel("Confirmar Contraseña:"))
        self.confirm_input = self.create_styled_input("Repite la contraseña")
        self.layout.addWidget(self.confirm_input['container'])

        # Mensaje de estado
        self.status_label = QLabel("")
        self.status_label.setMinimumHeight(20)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setProperty("class", "secondary")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.accept_btn = QPushButton("Crear Bóveda")
        self.accept_btn.setProperty("class", "primary")
        self.accept_btn.setMinimumHeight(45)
        self.accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_btn.clicked.connect(self.validate_and_accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.accept_btn)
        self.layout.addLayout(btn_layout)

        # Validación en tiempo real
        self.pwd_input['input'].textChanged.connect(self.check_passwords)
        self.confirm_input['input'].textChanged.connect(self.check_passwords)

    def check_passwords(self):
        p1 = self.pwd_input['input'].text()
        p2 = self.confirm_input['input'].text()
        
        if not p1:
            self.status_label.setText("")
            return
            
        if p1 != p2:
            self.status_label.setText("Las contraseñas no coinciden")
            self.status_label.setStyleSheet("color: #ff6b6b; font-size: 13px; font-weight: bold;")
        else:
            self.status_label.setText("¡Las contraseñas coinciden!")
            self.status_label.setStyleSheet("color: #4caf50; font-size: 13px; font-weight: bold;")

    def validate_and_accept(self):
        p1 = self.pwd_input['input'].text()
        p2 = self.confirm_input['input'].text()
        
        if len(p1) < 1:
            self.status_label.setText("Ingresa una contraseña")
            self.status_label.setStyleSheet("color: #ff6b6b; font-size: 13px; font-weight: bold;")
            return
            
        if p1 != p2:
            self.status_label.setText("Las contraseñas no coinciden")
            self.status_label.setStyleSheet("color: #ff6b6b; font-size: 13px; font-weight: bold;")
            return
            
        self.accept()
    
    def get_password(self):
        return self.pwd_input['input'].text()

class EnterPasswordDialog(BasePasswordDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Abrir Bóveda")
        
        self.create_header("Desbloquear Bóveda", 
                         "Ingresa tu contraseña maestra para acceder a tus datos.")

        # Input
        self.pwd_input = self.create_styled_input("Contraseña maestra")
        self.layout.addWidget(self.pwd_input['container'])
        
        # Mensaje de error (oculto por defecto)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff6b6b; font-size: 13px; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.error_label)
        
        self.layout.addStretch()

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setProperty("class", "secondary")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.accept_btn = QPushButton("Desbloquear")
        self.accept_btn.setProperty("class", "primary")
        self.accept_btn.setMinimumHeight(45)
        self.accept_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.accept_btn.clicked.connect(self.validate_and_accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.accept_btn)
        self.layout.addLayout(btn_layout)
        
        # Enter key triggers accept
        self.pwd_input['input'].returnPressed.connect(self.validate_and_accept)

    def validate_and_accept(self):
        pwd = self.pwd_input['input'].text()
        if not pwd:
            self.error_label.setText("Por favor ingresa la contraseña")
            return
        self.accept()

    def get_password(self):
        return self.pwd_input['input'].text()
