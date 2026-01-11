"""
Vista de autenticación
Permite crear o abrir una base de datos KeePass
"""
import flet as ft
from pathlib import Path


class AuthView(ft.Container):
    """Vista de autenticación para crear/abrir base de datos"""
    
    def __init__(self, page: ft.Page, on_auth_success):
        super().__init__()
        self._page = page
        self.on_auth_success = on_auth_success
        
        # Variables
        self.selected_file = None
        self.is_create_mode = True
        
        # Campo para ruta del archivo
        self.file_path_field = ft.TextField(
            label="Ruta del archivo .kdbx",
            hint_text="/home/usuario/mi_base_datos.kdbx",
            width=500,
            visible=False,
            border_radius=10,
            bgcolor="#2b2b2b",
        )
        
        # Campos de entrada
        self.password_field = ft.TextField(
            label="Contraseña maestra",
            password=True,
            can_reveal_password=True,
            width=350,
            border_radius=10,
            bgcolor="#2b2b2b",
        )
        
        self.file_path_text = ft.Text(
            "Ningún archivo seleccionado",
            size=14,
            color="#999999",
        )
        
        # Botones
        self.create_btn = ft.ElevatedButton(
            "Crear nueva base de datos",
            icon=ft.icons.Icons.CREATE_NEW_FOLDER,
            on_click=self.on_create_mode,
            style=ft.ButtonStyle(
                bgcolor="#1976d2",
                color="#ffffff",
                padding=15,
            )
        )
        
        self.open_btn = ft.OutlinedButton(
            "Abrir base de datos existente",
            icon=ft.icons.Icons.FOLDER_OPEN,
            on_click=self.on_open_mode,
            style=ft.ButtonStyle(
                padding=15,
            )
        )
        
        # Removido - ya no se usa FilePicker
        
        self.submit_btn = ft.ElevatedButton(
            "Continuar",
            icon=ft.icons.Icons.ARROW_FORWARD,
            on_click=self.on_submit,
            visible=False,
            style=ft.ButtonStyle(
                bgcolor="#4caf50",
                color="#ffffff",
                padding=15,
            )
        )
        
        self.back_btn = ft.TextButton(
            "← Volver",
            on_click=self.on_back,
            visible=False,
        )
        
        self.error_text = ft.Text(
            "",
            color="#f44336",
            size=14,
            visible=False,
        )
        
        # Construir UI
        self.content = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Icon(
                    ft.icons.Icons.LOCK,
                    size=80,
                    color="#1976d2",
                ),
                ft.Container(height=20),
                ft.Text(
                    "Password Manager",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Gestor de contraseñas seguro",
                    size=16,
                    color="#999999",
                ),
                ft.Container(height=40),
                self.create_btn,
                ft.Container(height=10),
                self.open_btn,
                ft.Container(height=30),
                self.back_btn,
                ft.Container(height=10),
                self.file_path_field,
                ft.Container(height=20),
                self.password_field,
                ft.Container(height=20),
                self.submit_btn,
                ft.Container(height=10),
                self.error_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)
    
    def on_create_mode(self, e):
        """Modo: crear nueva base de datos"""
        self.is_create_mode = True
        self.show_file_selection()
    
    def on_open_mode(self, e):
        """Modo: abrir base de datos existente"""
        self.is_create_mode = False
        self.show_file_selection()
    
    def show_file_selection(self):
        """Muestra los controles para seleccionar archivo"""
        self.create_btn.visible = False
        self.open_btn.visible = False
        self.back_btn.visible = True
        self.file_path_field.visible = True
        self.password_field.visible = True
        self.submit_btn.visible = True
        self.error_text.visible = False
        
        if self.is_create_mode:
            self.file_path_field.label = "Ruta donde guardar la base de datos"
            self.file_path_field.hint_text = "/home/usuario/passwords.kdbx"
            self.file_path_field.value = ""
        else:
            self.file_path_field.label = "Ruta del archivo .kdbx existente"
            self.file_path_field.hint_text = "/home/usuario/passwords.kdbx"
            self.file_path_field.value = ""
        
        self.update()
    
    def on_back(self, e):
        """Volver al menú principal"""
        self.reset_view()
    
    def reset_view(self):
        """Resetear la vista al estado inicial"""
        self.create_btn.visible = True
        self.open_btn.visible = True
        self.back_btn.visible = False
        self.file_path_field.visible = False
        self.file_path_field.value = ""
        self.password_field.visible = False
        self.password_field.value = ""
        self.submit_btn.visible = False
        self.error_text.visible = False
        self.selected_file = None
        self.update()
    
    def on_submit(self, e):
        """Procesar autenticación"""
        # Obtener la ruta del archivo del campo de texto
        file_path = self.file_path_field.value.strip()
        
        # Validar
        if not file_path:
            self.show_error("Por favor ingresa la ruta del archivo")
            return
        
        # Asegurar que tenga extensión .kdbx
        if not file_path.endswith('.kdbx'):
            file_path += '.kdbx'
        
        # Expandir ~ a home directory
        if file_path.startswith('~'):
            from os.path import expanduser
            file_path = expanduser(file_path)
        
        self.selected_file = file_path
        
        if not self.password_field.value:
            self.show_error("Por favor ingresa una contraseña")
            return
        
        # Intentar crear/abrir base de datos
        success = self.on_auth_success(
            self.selected_file,
            self.password_field.value,
            self.is_create_mode
        )
        
        if not success:
            if self.is_create_mode:
                self.show_error("Error al crear la base de datos")
            else:
                self.show_error("Contraseña incorrecta o archivo inválido")
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        self.error_text.value = message
        self.error_text.visible = True
        self.update()
