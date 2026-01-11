import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from src.database import Database
from src.ui.start_screen import StartScreen
from src.ui.main_window import MainWindow
from src.ui.styles import DARK_THEME

class KeyflowApp(QApplication):
    def __init__(self, argv):
        import os
        # Suprimir warnings benignos de Qt
        os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland*.debug=false;qt.qpa.wayland.textinput=false;qt.qpa.services=false"
        
        super().__init__(argv)
        
        # Configurar nombre de aplicación para integración con el sistema
        self.setApplicationName("keyflow")
        self.setOrganizationName("Keyflow")
        self.setApplicationDisplayName("Keyflow Password Manager")
        
        # Establecer el desktop file name para integración con GNOME/Ubuntu dock
        self.setDesktopFileName("keyflow")
        
        self.setStyle("Fusion")
        self.setStyleSheet(DARK_THEME)
        
        self.db = Database()
        
        self.settings = QSettings("Keyflow", "KeyflowApp")
        
        self.stack = QStackedWidget()
        self.stack.setWindowTitle("Keyflow")
        self.stack.resize(900, 600)
        
        import os
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            self.stack.setWindowIcon(QIcon(icon_path))
        
        self.start_screen = StartScreen()
        self.start_screen.create_db_signal.connect(self.create_db)
        self.start_screen.open_db_signal.connect(self.open_db)
        
        self.stack.addWidget(self.start_screen)
        
        self.stack.show()

    def create_db(self, filepath, password):
        try:
            self.db.create(filepath, password)
            self.settings.setValue("last_vault", filepath)
            self.show_main_window()
        except Exception as e:
            QMessageBox.critical(self.stack, "Error", f"No se pudo crear la base de datos: {e}")

    def open_db(self, filepath, password):
        try:
            self.db.load(filepath, password)
            self.settings.setValue("last_vault", filepath)
            self.show_main_window()
        except Exception as e:
            QMessageBox.critical(self.stack, "Error", "Contraseña inválida o archivo corrupto.")

    def show_main_window(self):
        self.main_window = MainWindow(self.db)
        self.main_window.logout_signal.connect(self.logout)
        
        self.stack.addWidget(self.main_window)
        self.stack.setCurrentWidget(self.main_window)

    def logout(self):
        self.stack.removeWidget(self.main_window)
        self.main_window.deleteLater()
        self.main_window = None
        self.db.kp = None
        self.stack.setCurrentWidget(self.start_screen)

def main():
    app = KeyflowApp(sys.argv)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
