"""
Vista del vault (bóveda de contraseñas)
Muestra y gestiona todas las contraseñas
"""
import flet as ft



class VaultView(ft.Container):
    """Vista principal del vault de contraseñas"""
    
    def __init__(self, page: ft.Page, keepass_manager, on_logout):
        super().__init__()
        self._page = page
        self.keepass_manager = keepass_manager
        self.on_logout = on_logout
        self.entries = []
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            hint_text="Buscar contraseñas...",
            prefix_icon=ft.icons.Icons.SEARCH,
            border_radius=10,
            bgcolor="#2b2b2b",
            on_change=self.on_search,
            expand=True,
        )
        
        # Lista de contraseñas
        self.password_list = ft.ListView(
            spacing=10,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            expand=True,
        )
        
        # Botones de la barra superior
        self.add_btn = ft.IconButton(
            icon=ft.icons.Icons.ADD,
            icon_size=30,
            tooltip="Añadir contraseña",
            on_click=self.show_add_dialog,
            icon_color="#4caf50",
        )
        
        self.logout_btn = ft.IconButton(
            icon=ft.icons.Icons.LOGOUT,
            icon_size=30,
            tooltip="Cerrar base de datos",
            on_click=lambda e: on_logout(),
            icon_color="#f44336",
        )
        
        # Construir UI
        self.content = ft.Column(
            controls=[
                # Barra superior
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.Icons.SHIELD, size=30, color="#1976d2"),
                            ft.Text("Mis Contraseñas", size=24, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            self.add_btn,
                            self.logout_btn,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor="#2b2b2b",
                    padding=15,
                    border_radius=10,
                ),
                ft.Container(height=20),
                # Búsqueda
                self.search_field,
                # Lista de contraseñas
                ft.Container(
                    content=self.password_list,
                    expand=True,
                ),
            ],
            expand=True,
        )
        
        self.padding = 20
        self.expand = True
    
    def load_passwords(self, query: str = ""):
        """Cargar y mostrar contraseñas"""
        if query:
            self.entries = self.keepass_manager.search_entries(query)
        else:
            self.entries = self.keepass_manager.get_all_entries()
        
        self.password_list.controls.clear()
        
        if not self.entries:
            self.password_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.icons.Icons.INBOX, size=80, color="#999999"),
                            ft.Text(
                                "No hay contraseñas guardadas" if not query else "No se encontraron resultados",
                                size=18,
                                color="#999999",
                            ),
                            ft.Text(
                                "Haz clic en + para añadir una nueva" if not query else "Intenta con otro término de búsqueda",
                                size=14,
                                color="#999999",
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                    expand=True,
                )
            )
        else:
            for entry in self.entries:
                self.password_list.controls.append(
                    self.create_password_card(entry)
                )
        
        self.update()
    
    def create_password_card(self, entry: dict) -> ft.Container:
        """Crear tarjeta para una contraseña"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Icono
                    ft.Container(
                        content=ft.Icon(ft.icons.Icons.KEY, size=30, color="#1976d2"),
                        padding=10,
                    ),
                    # Información
                    ft.Column(
                        controls=[
                            ft.Text(entry['title'], size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(entry['username'], size=14, color="#999999"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    # Botones de acción
                    ft.IconButton(
                        icon=ft.icons.Icons.COPY,
                        tooltip="Copiar contraseña",
                        on_click=lambda e, pw=entry['password']: self.copy_password(pw),
                        icon_color="#1976d2",
                    ),
                    ft.IconButton(
                        icon=ft.icons.Icons.VISIBILITY,
                        tooltip="Ver detalles",
                        on_click=lambda e, ent=entry: self.show_details_dialog(ent),
                        icon_color="#4caf50",
                    ),
                    ft.IconButton(
                        icon=ft.icons.Icons.EDIT,
                        tooltip="Editar",
                        on_click=lambda e, ent=entry: self.show_edit_dialog(ent),
                        icon_color="#ff9800",
                    ),
                    ft.IconButton(
                        icon=ft.icons.Icons.DELETE,
                        tooltip="Eliminar",
                        on_click=lambda e, uid=entry['uuid']: self.confirm_delete(uid),
                        icon_color="#f44336",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor="#2b2b2b",
            border_radius=10,
            padding=10,
        )
    
    def copy_password(self, password: str):
        """Copiar contraseña al portapapeles"""
        try:
            # Compatibilidad con diferentes versiones de Flet
            if hasattr(self._page, 'set_clipboard'):
                self._page.set_clipboard(password)
            else:
                self._page.clipboard = password
            
            self._page.update()
            self.show_snackbar("Contraseña copiada al portapapeles", "#4caf50")
        except Exception as e:
            print(f"Error al copiar: {e}")
            self.show_snackbar("Error al copiar contraseña", "#f44336")
    
    def on_search(self, e):
        """Buscar contraseñas"""
        self.load_passwords(self.search_field.value)
    
    def show_add_dialog(self, e):
        """Mostrar diálogo para añadir contraseña"""
        print("DEBUG: show_add_dialog called")  # Debug
        title_field = ft.TextField(label="Título *", autofocus=True)
        username_field = ft.TextField(label="Usuario *")
        password_field = ft.TextField(label="Contraseña *", password=True, can_reveal_password=True)
        url_field = ft.TextField(label="URL (opcional)")
        notes_field = ft.TextField(label="Notas (opcional)", multiline=True, min_lines=3)
        
        def save_entry(e):
            if not title_field.value or not username_field.value or not password_field.value:
                self.show_snackbar("Por favor completa los campos obligatorios", "#f44336")
                return
            
            success = self.keepass_manager.add_entry(
                title=title_field.value,
                username=username_field.value,
                password=password_field.value,
                url=url_field.value or "",
                notes=notes_field.value or ""
            )
            
            if success:
                self.show_snackbar("Contraseña añadida correctamente", "#4caf50")
                self.load_passwords()
                dialog.open = False
                self._page.update()
            else:
                self.show_snackbar("Error al añadir contraseña", "#f44336")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Añadir contraseña"),
            content=ft.Column(
                controls=[
                    title_field,
                    username_field,
                    password_field,
                    url_field,
                    notes_field,
                ],
                tight=True,
                width=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dialog)),
                ft.ElevatedButton("Guardar", on_click=save_entry),
            ],
        )
        
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()
    
    def show_edit_dialog(self, entry: dict):
        """Mostrar diálogo para editar contraseña"""
        title_field = ft.TextField(label="Título *", value=entry['title'])
        username_field = ft.TextField(label="Usuario *", value=entry['username'])
        password_field = ft.TextField(label="Contraseña *", value=entry['password'], 
                                      password=True, can_reveal_password=True)
        url_field = ft.TextField(label="URL (opcional)", value=entry['url'])
        notes_field = ft.TextField(label="Notas (opcional)", value=entry['notes'], 
                                   multiline=True, min_lines=3)
        
        def update_entry(e):
            if not title_field.value or not username_field.value or not password_field.value:
                self.show_snackbar("Por favor completa los campos obligatorios", "#f44336")
                return
            
            success = self.keepass_manager.update_entry(
                uuid=entry['uuid'],
                title=title_field.value,
                username=username_field.value,
                password=password_field.value,
                url=url_field.value or "",
                notes=notes_field.value or ""
            )
            
            if success:
                self.show_snackbar("Contraseña actualizada correctamente", "#4caf50")
                self.load_passwords()
                dialog.open = False
                self._page.update()
            else:
                self.show_snackbar("Error al actualizar contraseña", "#f44336")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar contraseña"),
            content=ft.Column(
                controls=[
                    title_field,
                    username_field,
                    password_field,
                    url_field,
                    notes_field,
                ],
                tight=True,
                width=400,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dialog)),
                ft.ElevatedButton("Guardar", on_click=update_entry),
            ],
        )
        
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()
    
    def show_details_dialog(self, entry: dict):
        """Mostrar diálogo con detalles de la contraseña"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(entry['title']),
            content=ft.Column(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.Icons.PERSON),
                        title=ft.Text("Usuario"),
                        subtitle=ft.Text(entry['username']),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.Icons.LOCK),
                        title=ft.Text("Contraseña"),
                        subtitle=ft.Text("•" * 12),
                        trailing=ft.IconButton(
                            icon=ft.icons.Icons.COPY,
                            on_click=lambda e: self.copy_password(entry['password']),
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.Icons.LINK),
                        title=ft.Text("URL"),
                        subtitle=ft.Text(entry['url'] or "No especificada"),
                    ) if entry['url'] else ft.Container(),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Notas:", weight=ft.FontWeight.BOLD),
                                ft.Text(entry['notes'] or "Sin notas"),
                            ]
                        ),
                        padding=10,
                    ) if entry['notes'] else ft.Container(),
                ],
                tight=True,
                width=400,
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog(dialog)),
            ],
        )
        
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()
    
    def confirm_delete(self, uuid: str):
        """Confirmar eliminación de contraseña"""
        def delete_entry(e):
            success = self.keepass_manager.delete_entry(uuid)
            if success:
                self.show_snackbar("Contraseña eliminada correctamente", "#4caf50")
                self.load_passwords()
                dialog.open = False
                self._page.update()
            else:
                self.show_snackbar("Error al eliminar contraseña", "#f44336")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Estás seguro de que quieres eliminar esta contraseña?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dialog)),
                ft.ElevatedButton(
                    "Eliminar",
                    on_click=delete_entry,
                    style=ft.ButtonStyle(bgcolor="#f44336"),
                ),
            ],
        )
        
        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()
    
    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self._page.update()
    
    def show_snackbar(self, message: str, color):
        """Mostrar mensaje temporal"""
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
        )
        self._page.snack_bar = snackbar
        snackbar.open = True
        self._page.update()
