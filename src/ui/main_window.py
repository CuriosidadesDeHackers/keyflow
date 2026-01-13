import uuid
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QHeaderView, QMessageBox, QMenu, QLabel, QLineEdit, QProgressBar)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QGuiApplication, QKeySequence

from .entry_dialog import EntryDialog
from .security_audit_dialog import SecurityAuditDialog

class MainWindow(QMainWindow):
    logout_signal = Signal()

    def __init__(self, db_helper):
        super().__init__()
        self.setWindowTitle("Gestor de Contraseñas Keyflow")
        self.resize(1000, 700)
        
        self.db = db_helper
        
        self.all_entries = []
        
        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.update_clipboard_countdown)
        self.clipboard_remaining = 0
        self.clipboard_duration = 12
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        self.create_menu_bar()
        
        self.header_layout = QHBoxLayout()
        self.db_label = QLabel(f"Bóveda: {self.db.filepath}")
        self.db_label.setStyleSheet("color:")
        self.header_layout.addWidget(self.db_label)
        self.header_layout.addStretch()
        
        self.logout_btn = QPushButton("Cerrar Bóveda")
        self.logout_btn.setStyleSheet("background-color:")
        self.logout_btn.clicked.connect(self.logout)
        self.header_layout.addWidget(self.logout_btn)
        
        self.layout.addLayout(self.header_layout)

        self.toolbar_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Agregar Entrada")
        self.add_btn.setProperty("class", "primary")
        self.add_btn.clicked.connect(self.add_entry)
        self.toolbar_layout.addWidget(self.add_btn)
        


        self.toolbar_layout.addStretch()
        
        # Campo de búsqueda
        self.search_label = QLabel("Buscar:")
        self.toolbar_layout.addWidget(self.search_label)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar por título, usuario, URL o notas...")
        self.search_field.setMinimumWidth(300)
        self.search_field.textChanged.connect(self.filter_entries)
        self.search_field.setClearButtonEnabled(True)
        self.toolbar_layout.addWidget(self.search_field)
        
        self.layout.addLayout(self.toolbar_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["UUID", "Título", "Usuario", "URL", "Notas", "Modificado"])
        
        # Configurar anchos de columna
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # Título ocupa el espacio disponible
        self.table.setColumnWidth(2, 200) # Usuario
        self.table.setColumnWidth(3, 180) # URL
        self.table.setColumnWidth(4, 150) # Notas
        self.table.setColumnWidth(5, 150) # Modificado
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.edit_entry)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Permitir ordenar por columnas al hacer clic en los encabezados
        self.table.setSortingEnabled(True)
        
        self.layout.addWidget(self.table)
        
        # Barra de progreso del portapapeles
        self.clipboard_progress = QProgressBar()
        self.clipboard_progress.setMaximum(self.clipboard_duration * 10)  # 10 updates por segundo
        self.clipboard_progress.setTextVisible(True)
        self.clipboard_progress.setFormat("Portapapeles se limpiará en %v segundos")
        self.clipboard_progress.setVisible(False)
        self.clipboard_progress.setMaximumHeight(20)
        self.layout.addWidget(self.clipboard_progress)
        
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color:")
        
        self.load_entries()
        QTimer.singleShot(0, self.search_field.setFocus)

    def logout(self):
        self.db.save()
        self.logout_signal.emit()

    def load_entries(self):
        """Carga todas las entradas desde la base de datos"""
        entries = self.db.get_entries()
        self.all_entries = list(entries)
        self.all_entries.sort(key=lambda x: x.title if x.title else "")
        
        # Limpiar el campo de búsqueda y mostrar todas las entradas
        self.search_field.clear()
        self.display_entries(self.all_entries)
    
    def filter_entries(self):
        """Filtra las entradas basándose en el texto de búsqueda"""
        search_text = self.search_field.text().lower().strip()
        
        if not search_text:
            # Si no hay texto de búsqueda, mostrar todas las entradas
            self.display_entries(self.all_entries)
            return
        
        # Filtrar entradas que contengan el texto de búsqueda en título, usuario, URL o notas
        filtered = []
        for entry in self.all_entries:
            title = (entry.title or "").lower()
            username = (entry.username or "").lower()
            url = (entry.url or "").lower()
            notes = (entry.notes or "").lower()
            
            if (search_text in title or 
                search_text in username or 
                search_text in url or 
                search_text in notes):
                filtered.append(entry)
        
        self.display_entries(filtered)
    
    def display_entries(self, entries):
        """Muestra las entradas proporcionadas en la tabla"""
        # Desactivar sorting durante la actualización para evitar problemas de índices y rendimiento
        sorting_enabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        
        self.table.setRowCount(0)
        
        for row, entry in enumerate(entries):
            uuid = str(entry.uuid)
            title = entry.title or ""
            username = entry.username or ""
            url = entry.url or ""
            notes = entry.notes or ""
            
            # Obtener emoji de la entrada
            emoji = entry.get_custom_property("emoji") or ""
            
            # Combinar emoji con título
            display_title = f"{emoji} {title}" if emoji else title
            
            # Formatear fecha de modificación
            mtime_str = ""
            if hasattr(entry, 'mtime') and entry.mtime:
                mtime_str = entry.mtime.strftime("%Y-%m-%d %H:%M")

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(uuid))
            self.table.setItem(row, 1, QTableWidgetItem(display_title))
            self.table.setItem(row, 2, QTableWidgetItem(username))
            self.table.setItem(row, 3, QTableWidgetItem(url))
            self.table.setItem(row, 4, QTableWidgetItem(notes))
            self.table.setItem(row, 5, QTableWidgetItem(mtime_str))
        
        # Actualizar la barra de estado con el número de entradas mostradas
        total = len(self.all_entries)
        shown = len(entries)
        if shown < total:
            self.status_bar.showMessage(f"Mostrando {shown} de {total} entradas", 3000)
        else:
            self.status_bar.clearMessage()
            
        self.table.setSortingEnabled(sorting_enabled)

    def add_entry(self):
        dialog = EntryDialog(self, title="New Entry")
        if dialog.exec():
            title, user, pwd, url, notes, emoji = dialog.get_data()  # Ahora retorna 6 valores
            if not title:
                QMessageBox.warning(self, "Error", "El título es obligatorio")
                return
                
            try:
                self.db.add_entry(title, user, pwd, url, notes, emoji)
                self.load_entries()
                self.status_bar.showMessage("Entrada agregada correctamente", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar entrada: {e}")

    def edit_entry(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        uuid_str = self.table.item(row, 0).text()
        entry = self.db.kp.find_entries(uuid=uuid.UUID(uuid_str), first=True)
        if not entry:
            return
        
        # Obtener emoji de la entrada
        emoji = entry.get_custom_property("emoji") or ""

        dialog = EntryDialog(self, 
                             entry.title or "", 
                             entry.username or "", 
                             entry.password or "", 
                             entry.url or "", 
                             entry.notes or "",
                             emoji)
                             
        if dialog.exec():
            new_title, new_user, new_pwd, new_url, new_notes, new_emoji = dialog.get_data()
            
            try:
                self.db.update_entry(entry.uuid, new_title, new_user, new_pwd, new_url, new_notes, new_emoji)
                self.load_entries()
                self.status_bar.showMessage("Entrada actualizada correctamente", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar entrada: {e}")

    def delete_entry(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        uuid_str = self.table.item(row, 0).text()
        
        confirm = QMessageBox.question(self, "Confirmar Eliminación", 
                                     "¿Está seguro de que desea eliminar esta entrada?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            self.db.delete_entry(uuid.UUID(uuid_str))
            self.load_entries()
            self.status_bar.showMessage("Entrada eliminada correctamente", 3000)

    def show_context_menu(self, position):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        url = self.table.item(row, 3).text()
        
        menu = QMenu()
        
        # Acciones de copiado (Prioridad alta)
        copy_user_action = menu.addAction("Copiar Usuario")
        copy_pass_action = menu.addAction("Copiar Contraseña")
        
        copy_url_action = None
        if url and url.strip():
            copy_url_action = menu.addAction("Copiar URL")
            
        menu.addSeparator()
        
        # Acciones de edición (Prioridad baja)
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Eliminar")
        
        action = menu.exec(self.table.viewport().mapToGlobal(position))
        
        if action == edit_action:
            self.edit_entry()
        elif action == delete_action:
            self.delete_entry()
        elif action == copy_user_action:
            self.copy_field(2)
        elif action == copy_pass_action:
            self.copy_password()
        elif copy_url_action and action == copy_url_action:
            self.copy_field(3)

    def copy_field(self, col_index):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        text = self.table.item(row, col_index).text()
        QGuiApplication.clipboard().setText(text)
        self.start_clipboard_timer()

    def copy_password(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        uuid_str = self.table.item(row, 0).text()
        
        
        entry = self.db.kp.find_entries(uuid=uuid.UUID(uuid_str), first=True)
        if entry and entry.password:
            QGuiApplication.clipboard().setText(entry.password)
            self.start_clipboard_timer()

    def start_clipboard_timer(self):
        """Start 12-second countdown to clear clipboard"""
        self.clipboard_remaining = self.clipboard_duration * 10  # 10 ticks por segundo
        self.clipboard_progress.setValue(self.clipboard_remaining)
        self.clipboard_progress.setVisible(True)
        self.clipboard_timer.start(100)  # 100ms intervals (10 veces por segundo)
        self.update_clipboard_countdown()

    def update_clipboard_countdown(self):
        """Update progress bar with remaining time"""
        if self.clipboard_remaining > 0:
            self.clipboard_remaining -= 1
            self.clipboard_progress.setValue(self.clipboard_remaining)
            # Actualizar el texto para mostrar segundos
            seconds_left = (self.clipboard_remaining + 9) // 10  # Redondear hacia arriba
            self.clipboard_progress.setFormat(f"Portapapeles se limpiará en {seconds_left} segundos")
        else:
            self.clipboard_timer.stop()
            self.clipboard_progress.setVisible(False)
            QGuiApplication.clipboard().clear()
            self.status_bar.showMessage("Portapapeles limpiado", 3000)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&Archivo")

        save_action = QAction("&Guardar", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.db.save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        close_vault_action = QAction("Cerrar &Bóveda", self)
        close_vault_action.triggered.connect(self.logout)
        file_menu.addAction(close_vault_action)
        
        exit_action = QAction("&Salir", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("&Editar")

        add_action = QAction("&Agregar Entrada", self)
        add_action.setShortcut(QKeySequence.New)
        add_action.triggered.connect(self.add_entry)
        edit_menu.addAction(add_action)

        edit_entry_action = QAction("&Editar Entrada", self)
        edit_entry_action.triggered.connect(self.edit_entry)
        edit_menu.addAction(edit_entry_action)
        
        delete_action = QAction("E&liminar Entrada", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self.delete_entry)
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        copy_user_action = QAction("Copiar &Usuario", self)
        copy_user_action.triggered.connect(lambda: self.copy_field(2))
        edit_menu.addAction(copy_user_action)

        copy_pass_action = QAction("Copiar &Contraseña", self)
        copy_pass_action.triggered.connect(self.copy_password)
        edit_menu.addAction(copy_pass_action)

        help_menu = menubar.addMenu("A&yuda")

        audit_action = QAction("🛡️ Auditar seguridad de contraseñas", self)
        audit_action.triggered.connect(self.show_audit_dialog)
        help_menu.addAction(audit_action)
        
        help_menu.addSeparator()

        about_action = QAction("&Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.information(self, "Acerca de Keyflow", 
                              "Gestor de Contraseñas Keyflow\n\n"
                              "Un gestor de contraseñas seguro y de código abierto compatible con archivos .kdbx.\n"
                              "Desarrollado con Python y PySide6.\n\n"
                              "Autores : Maalfer & Santitub\n"
                              "GitHub: https://github.com/Maalfer/keyflow\n"
                              "LinkedIn: https://www.linkedin.com/in/maalfer1/")

    def show_audit_dialog(self):
        """Muestra el diálogo de auditoría de seguridad"""
        entries = self.db.get_entries()
        dialog = SecurityAuditDialog(entries, self)
        dialog.exec()