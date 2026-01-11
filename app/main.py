"""
Aplicación principal de gestión de contraseñas
"""
import flet as ft
from core.keepass import KeePassManager
from views.auth_view import AuthView
from views.vault_view import VaultView


class PasswordManagerApp:
    """Aplicación principal"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.keepass_manager = KeePassManager()
        
        # Configurar página
        self.page.title = "Password Manager"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.window_min_width = 700
        self.page.window_min_height = 500
        
        # Mostrar vista de autenticación
        self.show_auth_view()
    
    def show_auth_view(self):
        """Mostrar vista de autenticación"""
        auth_view = AuthView(self.page, self.on_auth_success)
        self.page.clean()
        self.page.add(auth_view)
        self.page.update()
    
    def show_vault_view(self):
        """Mostrar vista del vault"""
        vault_view = VaultView(self.page, self.keepass_manager, self.on_logout)
        self.page.clean()
        self.page.add(vault_view)
        self.page.update()
        # Cargar contraseñas después de añadir el control a la página
        vault_view.load_passwords()
    
    def on_auth_success(self, filepath: str, password: str, is_create: bool) -> bool:
        """
        Callback cuando la autenticación es exitosa
        
        Args:
            filepath: Ruta al archivo .kdbx
            password: Contraseña maestra
            is_create: True si se está creando, False si se está abriendo
            
        Returns:
            True si la operación fue exitosa
        """
        if is_create:
            success = self.keepass_manager.create_database(filepath, password)
        else:
            success = self.keepass_manager.open_database(filepath, password)
        
        if success:
            self.show_vault_view()
        
        return success
    
    def on_logout(self):
        """Cerrar sesión"""
        self.keepass_manager.close_database()
        self.show_auth_view()


def main(page: ft.Page):
    """Función principal"""
    PasswordManagerApp(page)


if __name__ == "__main__":
    ft.run(main)
