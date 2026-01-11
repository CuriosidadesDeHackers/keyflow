import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from src.database import Database
from src.ui.start_screen import StartScreen
from src.ui.main_window import MainWindow
from src.ui.styles import DARK_THEME

class KeyflowApp(QApplication):
    def __init__(self, argv):
        # Suppress Wayland noise
        import os
        os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland*.debug=false;qt.qpa.wayland.textinput=false"
        
        super().__init__(argv)
        self.setStyle("Fusion")
        self.setStyleSheet(DARK_THEME)
        
        self.db = Database()
        
        # Stacked Widget to manage screens
        self.stack = QStackedWidget()
        self.stack.setWindowTitle("Keyflow")
        self.stack.resize(900, 600)
        
        # Screens
        self.start_screen = StartScreen()
        self.start_screen.create_db_signal.connect(self.create_db)
        self.start_screen.open_db_signal.connect(self.open_db)
        
        self.stack.addWidget(self.start_screen)
        
        self.stack.show()

    def create_db(self, filepath, password):
        try:
            self.db.create(filepath, password)
            self.show_main_window()
        except Exception as e:
            QMessageBox.critical(self.stack, "Error", f"Could not create database: {e}")

    def open_db(self, filepath, password):
        try:
            self.db.load(filepath, password)
            self.show_main_window()
        except Exception as e:
            QMessageBox.critical(self.stack, "Error", "Invalid password or corrupted file.")

    def show_main_window(self):
        self.main_window = MainWindow(self.db)
        self.main_window.logout_signal.connect(self.logout)
        
        # We replace the stack content or just hide it and show main window?
        # Let's use stack for simple navigation
        self.stack.addWidget(self.main_window)
        self.stack.setCurrentWidget(self.main_window)

    def logout(self):
        self.stack.removeWidget(self.main_window)
        self.main_window.deleteLater()
        self.main_window = None
        self.db.kp = None # Clear database from memory
        self.stack.setCurrentWidget(self.start_screen)

if __name__ == "__main__":
    app = KeyflowApp(sys.argv)
    sys.exit(app.exec())
