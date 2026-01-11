from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QPushButton, QWidget)
from PySide6.QtCore import Qt

class EntryDialog(QDialog):
    def __init__(self, parent=None, title="", username="", password="", url="", notes=""):
        super().__init__(parent)
        self.setWindowTitle("Entry Details")
        
        self.setModal(True)
        self.resize(500, 600)  # Larger, modern size
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header = QLabel(title or "Entry Details")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Form Container
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        # Title
        form_layout.addWidget(QLabel("Title"))
        self.title_input = QLineEdit(title)
        self.title_input.setPlaceholderText("e.g. Google Account")
        form_layout.addWidget(self.title_input)
        
        # Username
        form_layout.addWidget(QLabel("Username"))
        self.user_input = QLineEdit(username)
        self.user_input.setPlaceholderText("email@example.com")
        form_layout.addWidget(self.user_input)
        
        # Password with Toggle
        form_layout.addWidget(QLabel("Password"))
        pass_layout = QHBoxLayout()
        self.pass_input = QLineEdit(password)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("••••••••")
        
        self.toggle_btn = QPushButton("Show")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedWidth(60)
        self.toggle_btn.clicked.connect(self.toggle_password)
        
        self.gen_btn = QPushButton("Generate")
        self.gen_btn.setFixedWidth(80)
        self.gen_btn.setStyleSheet("background-color: #2d2d2d; border: 1px solid #555555;")
        self.gen_btn.clicked.connect(self.generate_password)
        
        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(self.toggle_btn)
        pass_layout.addWidget(self.gen_btn)
        form_layout.addLayout(pass_layout)

        # URL
        form_layout.addWidget(QLabel("URL"))
        self.url_input = QLineEdit(url)
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addWidget(self.url_input)
        
        # Notes
        form_layout.addWidget(QLabel("Notes"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(notes)
        self.notes_input.setPlaceholderText("Additional details...")
        self.notes_input.setFixedHeight(120)  # Reasonable height for notes
        form_layout.addWidget(self.notes_input)
        
        layout.addLayout(form_layout)
        
        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setProperty("role", "primary")  # Use primary style
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)

    def toggle_password(self, checked):
        if checked:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")

    def generate_password(self):
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        
        self.pass_input.setText(password)
        
        # Auto-show
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.setText("Hide")

    def get_data(self):
        return (
            self.title_input.text(),
            self.user_input.text(),
            self.pass_input.text(),
            self.url_input.text(),
            self.notes_input.toPlainText()
        )
