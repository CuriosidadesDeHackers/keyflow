from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt

class MasterPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Establecer Contraseña Maestra")
        self.setFixedWidth(400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("Seguridad de la Bóveda")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #007acc; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        description = QLabel("Establece una contraseña maestra fuerte para proteger tus datos.")
        description.setWordWrap(True)
        description.setStyleSheet("color: #888888; margin-bottom: 10px;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Campo Contraseña
        layout.addWidget(QLabel("Contraseña Maestra:"))
        self.pwd_input = self.create_password_input()
        layout.addLayout(self.pwd_input['layout'])

        # Campo Confirmación
        layout.addWidget(QLabel("Confirmar Contraseña:"))
        self.confirm_input = self.create_password_input()
        layout.addLayout(self.confirm_input['layout'])

        # Mensaje de estado
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setProperty("class", "secondary")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.accept_btn = QPushButton("Crear Bóveda")
        self.accept_btn.setProperty("class", "primary")
        self.accept_btn.setMinimumHeight(40)
        self.accept_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addWidget(self.accept_btn)

        layout.addLayout(btn_layout)

        # Conectar validación en tiempo real
        self.pwd_input['input'].textChanged.connect(self.check_passwords)
        self.confirm_input['input'].textChanged.connect(self.check_passwords)

    def create_password_input(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        
        inp = QLineEdit()
        inp.setEchoMode(QLineEdit.EchoMode.Password)
        inp.setMinimumHeight(35)
        layout.addWidget(inp)
        
        toggle = QPushButton("👁️")
        toggle.setFixedWidth(40)
        toggle.setMinimumHeight(35)
        toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle.pressed.connect(lambda: inp.setEchoMode(QLineEdit.EchoMode.Normal))
        toggle.released.connect(lambda: inp.setEchoMode(QLineEdit.EchoMode.Password))
        layout.addWidget(toggle)
        
        return {'layout': layout, 'input': inp}

    def check_passwords(self):
        p1 = self.pwd_input['input'].text()
        p2 = self.confirm_input['input'].text()
        
        if not p1:
            self.status_label.setText("")
            return False
            
        if p1 != p2:
            self.status_label.setText("Las contraseñas no coinciden")
            self.status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
        else:
            self.status_label.setText("Las contraseñas coinciden")
            self.status_label.setStyleSheet("color: #4caf50; font-size: 12px;")

    def validate_and_accept(self):
        p1 = self.pwd_input['input'].text()
        p2 = self.confirm_input['input'].text()
        
        if not p1:
            self.status_label.setText("La contraseña no puede estar vacía")
            self.status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
            return
            
        if p1 != p2:
            self.status_label.setText("Las contraseñas no coinciden")
            self.status_label.setStyleSheet("color: #d32f2f; font-size: 12px;")
            return
            
        self.accept()
    
    def get_password(self):
        return self.pwd_input['input'].text()
