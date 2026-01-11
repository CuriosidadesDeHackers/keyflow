from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QHeaderView, QMessageBox, QMenu, QLabel, QLineEdit)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QClipboard, QGuiApplication, QKeySequence

from .entry_dialog import EntryDialog

class MainWindow(QMainWindow):
    logout_signal = Signal()

    def __init__(self, db_helper):
        super().__init__()
        self.setWindowTitle("Gestor de Contraseñas Keyflow")
        self.resize(1000, 700)
        
        self.db = db_helper
        
        # Lista para almacenar todas las entradas
        self.all_entries = []
        
        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.update_clipboard_countdown)
        self.clipboard_remaining = 0
        
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
        
        self.add_btn = QPushButton("➕ Agregar Entrada")
        self.add_btn.setProperty("class", "primary")
        self.add_btn.clicked.connect(self.add_entry)
        self.toolbar_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setStyleSheet("background-color:")
        self.refresh_btn.clicked.connect(self.load_entries)
        self.toolbar_layout.addWidget(self.refresh_btn)

        self.toolbar_layout.addStretch()
        
        # Campo de búsqueda
        self.search_label = QLabel("🔍 Buscar:")
        self.toolbar_layout.addWidget(self.search_label)
        
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Buscar por título, usuario, URL o notas...")
        self.search_field.setMinimumWidth(300)
        self.search_field.textChanged.connect(self.filter_entries)
        self.search_field.setClearButtonEnabled(True)
        self.toolbar_layout.addWidget(self.search_field)
        
        self.layout.addLayout(self.toolbar_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["UUID", "Título", "Usuario", "URL", "Notas"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.edit_entry)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.table)
        
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color:")
        
        self.load_entries()

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
        self.table.setRowCount(0)
        
        for row, entry in enumerate(entries):
            uuid = str(entry.uuid)
            title = entry.title or ""
            username = entry.username or ""
            url = entry.url or ""
            notes = entry.notes or ""

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(uuid))
            self.table.setItem(row, 1, QTableWidgetItem(title))
            self.table.setItem(row, 2, QTableWidgetItem(username))
            self.table.setItem(row, 3, QTableWidgetItem(url))
            self.table.setItem(row, 4, QTableWidgetItem(notes))
        
        # Actualizar la barra de estado con el número de entradas mostradas
        total = len(self.all_entries)
        shown = len(entries)
        if shown < total:
            self.status_bar.showMessage(f"Mostrando {shown} de {total} entradas", 3000)
        else:
            self.status_bar.clearMessage()

    def add_entry(self):
        dialog = EntryDialog(self, title="New Entry")
        if dialog.exec():
            title, user, pwd, url, notes = dialog.get_data()
            if not title:
                QMessageBox.warning(self, "Error", "El título es obligatorio")
                return
                
            try:
                self.db.add_entry(title, user, pwd, url, notes)
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
        
        import uuid
        entry = self.db.kp.find_entries(uuid=uuid.UUID(uuid_str), first=True)
        if not entry:
            return

        dialog = EntryDialog(self, 
                             entry.title or "", 
                             entry.username or "", 
                             entry.password or "", 
                             entry.url or "", 
                             entry.notes or "")
                             
        if dialog.exec():
            new_title, new_user, new_pwd, new_url, new_notes = dialog.get_data()
            
            try:
                self.db.update_entry(entry.uuid, new_title, new_user, new_pwd, new_url, new_notes)
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
            import uuid
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
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Eliminar")
        menu.addSeparator()
        copy_user_action = menu.addAction("Copiar Usuario")
        copy_pass_action = menu.addAction("Copiar Contraseña")
        
        copy_url_action = None
        if url and url.strip():
            copy_url_action = menu.addAction("Copiar URL")
        
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
        
        import uuid
        entry = self.db.kp.find_entries(uuid=uuid.UUID(uuid_str), first=True)
        if entry and entry.password:
            QGuiApplication.clipboard().setText(entry.password)
            self.start_clipboard_timer()

    def start_clipboard_timer(self):
        """Start 12-second countdown to clear clipboard"""
        self.clipboard_remaining = 12
        self.clipboard_timer.start(1000)  # 1 second intervals
        self.update_clipboard_countdown()

    def update_clipboard_countdown(self):
        """Update status bar with remaining time"""
        if self.clipboard_remaining > 0:
            self.status_bar.showMessage(f"Portapapeles se limpiará en {self.clipboard_remaining} segundos...")
            self.clipboard_remaining -= 1
        else:
            self.clipboard_timer.stop()
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

        about_action = QAction("&Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.information(self, "Acerca de Keyflow", 
                              "Gestor de Contraseñas Keyflow\n\n"
                              "Un gestor de contraseñas seguro y de código abierto compatible con archivos .kdbx.\n"
                              "Desarrollado con Python y PySide6.\n\n"
                              "Autor: Maalfer\n"
                              "GitHub: https://github.com/Maalfer/keyflow\n"
                              "LinkedIn: https://www.linkedin.com/in/maalfer1/")
