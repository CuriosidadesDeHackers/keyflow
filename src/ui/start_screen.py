from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QFileDialog, QInputDialog, QMessageBox, QSpacerItem, QSizePolicy, QLineEdit)
from PySide6.QtCore import Qt, Signal

class StartScreen(QWidget):
    open_db_signal = Signal(str, str) # filepath, password
    create_db_signal = Signal(str, str) # filepath, password

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Title
        title = QLabel("Keyflow")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #007acc; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Secure Password Manager")
        subtitle.setStyleSheet("font-size: 16px; color: #888888; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons
        self.create_btn = QPushButton("Create New Database")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.clicked.connect(self.create_db)
        layout.addWidget(self.create_btn)

        self.open_btn = QPushButton("Open Existing Database")
        self.open_btn.setMinimumHeight(50)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border: 1px solid #3d3d3d;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.clicked.connect(self.open_db)
        layout.addWidget(self.open_btn)

        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_db(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Create New Database", "", "KeePass Databases (*.kdbx)")
        if filepath:
            if not filepath.endswith(".kdbx"):
                filepath += ".kdbx"
            
            pwd, ok = QInputDialog.getText(self, "Set Master Password", "Enter Master Password:", echo=QLineEdit.EchoMode.Password)
            if ok and pwd:
                confirm, ok2 = QInputDialog.getText(self, "Confirm Password", "Confirm Master Password:", echo=QLineEdit.EchoMode.Password)
                if ok2 and confirm == pwd:
                    self.create_db_signal.emit(filepath, pwd)
                elif ok2:
                     QMessageBox.warning(self, "Error", "Passwords do not match")
            elif ok:
                 QMessageBox.warning(self, "Error", "Password cannot be empty")

    def open_db(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Database", "", "KeePass Databases (*.kdbx)")
        if filepath:
            pwd, ok = QInputDialog.getText(self, "Enter Master Password", "Master Password:", echo=QLineEdit.EchoMode.Password)
            if ok:
                self.open_db_signal.emit(filepath, pwd)
