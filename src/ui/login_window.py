from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QDialog):
    def __init__(self, parent=None, is_registration=False):
        super().__init__(parent)
        self.setWindowTitle("Keyflow Login" if not is_registration else "Create Master Password")
        self.is_registration = is_registration
        self.password = None

        layout = QVBoxLayout(self)

        self.label = QLabel("Enter Master Password:" if not is_registration else "Create Master Password:")
        layout.addWidget(self.label)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        if is_registration:
            self.confirm_label = QLabel("Confirm Master Password:")
            layout.addWidget(self.confirm_label)
            self.confirm_edit = QLineEdit()
            self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(self.confirm_edit)

        self.submit_btn = QPushButton("Login" if not is_registration else "Create Database")
        self.submit_btn.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_btn)

    def handle_submit(self):
        pwd = self.password_edit.text()
        if not pwd:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return

        if self.is_registration:
            confirm = self.confirm_edit.text()
            if pwd != confirm:
                QMessageBox.warning(self, "Error", "Passwords do not match")
                return

        self.password = pwd
        self.accept()
