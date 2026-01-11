from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QTextEdit

class EntryDialog(QDialog):
    def __init__(self, parent=None, title="", username="", password="", url="", notes=""):
        super().__init__(parent)
        self.setWindowTitle("Entry Details")
        
        self.title_edit = QLineEdit(title)
        self.username_edit = QLineEdit(username)
        self.password_edit = QLineEdit(password)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.url_edit = QLineEdit(url)
        self.notes_edit = QTextEdit(notes)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        form_layout.addRow("Title:", self.title_edit)
        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Password:", self.password_edit)
        form_layout.addRow("URL:", self.url_edit)
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

    def get_data(self):
        return (
            self.title_edit.text(),
            self.username_edit.text(),
            self.password_edit.text(),
            self.url_edit.text(),
            self.notes_edit.toPlainText()
        )
