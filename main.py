import sys
import os
import platform
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtCore import QSettings, QTimer, QEvent
from PySide6.QtGui import QIcon
from src.database import Database
from src.ui.start_screen import StartScreen
from src.ui.main_window import MainWindow
from src.ui.styles import DARK_THEME

class KeyflowApp(QApplication):
    def __init__(self, argv):
        
        # Forzar el uso de X11 (xcb) para evitar problemas gráficos y de permisos en Wayland/GNOME.
        # Solo forzar X11 en Linux para evitar problemas con Wayland.
        if platform.system() == "Linux":
            os.environ["QT_QPA_PLATFORM"] = "xcb"
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
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
        if not os.path.exists(icon_path):
            print(f"Warning: Icon not found at {icon_path}")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            self.stack.setWindowIcon(QIcon(icon_path))
        
        self.start_screen = StartScreen()
        self.start_screen.create_db_signal.connect(self.create_db)
        self.start_screen.open_db_signal.connect(self.open_db)
        
        self.stack.addWidget(self.start_screen)
        
        self.stack.show()
        
        # Auto-Lock Timer
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.lock_application)
        self.inactivity_limit = 5 * 60 * 1000  # 5 minutos en milisegundos
        self.inactivity_timer.start(self.inactivity_limit)

    def notify(self, receiver, event):
        # Reset timer on user interaction
        if event.type() in (QEvent.KeyPress, QEvent.MouseButtonPress, QEvent.MouseMove, QEvent.Wheel):
            if hasattr(self, 'inactivity_timer'):
                self.inactivity_timer.start(self.inactivity_limit)
        return super().notify(receiver, event)

    def lock_application(self):
        # Only lock if we are currently logged in (showing MainWindow)
        if hasattr(self, 'main_window') and self.main_window and self.stack.currentWidget() == self.main_window:
            print("Auto-locking due to inactivity...")
            self.logout()
            QMessageBox.information(self.stack, "Bloqueo Automático", "La aplicación se ha bloqueado por inactividad.")

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
        # Restart timer ensuring we start counting from now
        self.inactivity_timer.start(self.inactivity_limit)

    def logout(self):
        if hasattr(self, 'main_window') and self.main_window:
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
