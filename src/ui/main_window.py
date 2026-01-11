from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QHeaderView, QMessageBox, QMenu, QLabel)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QClipboard, QGuiApplication, QKeySequence

from .entry_dialog import EntryDialog

class MainWindow(QMainWindow):
    logout_signal = Signal()

    def __init__(self, db_helper):
        super().__init__()
        self.setWindowTitle("Keyflow Password Manager")
        self.resize(1000, 700)
        
        self.db = db_helper
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        # Menu Bar
        self.create_menu_bar()
        
        # Header / Status
        self.header_layout = QHBoxLayout()
        self.db_label = QLabel(f"Vault: {self.db.filepath}")
        self.db_label.setStyleSheet("color: #888888; font-weight: bold;")
        self.header_layout.addWidget(self.db_label)
        self.header_layout.addStretch()
        
        self.logout_btn = QPushButton("Close Vault")
        self.logout_btn.setStyleSheet("background-color: #d32f2f; padding: 4px 12px;")
        self.logout_btn.clicked.connect(self.logout)
        self.header_layout.addWidget(self.logout_btn)
        
        self.layout.addLayout(self.header_layout)

        # Toolbar
        self.toolbar_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("+ Add Entry")
        self.add_btn.clicked.connect(self.add_entry)
        self.toolbar_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("background-color: #333333;")
        self.refresh_btn.clicked.connect(self.load_entries)
        self.toolbar_layout.addWidget(self.refresh_btn)

        self.toolbar_layout.addStretch()
        self.layout.addLayout(self.toolbar_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["UUID", "Title", "Username", "URL", "Notes"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # Title stretches
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch) # Notes stretches
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.hideColumn(0) # Hide UUID
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.edit_entry)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.table)
        
        self.load_entries()

    def logout(self):
        self.db.save()
        self.logout_signal.emit()

    def load_entries(self):
        self.table.setRowCount(0)
        entries = self.db.get_entries()
        
        # Sort entries by title for better UX
        entries.sort(key=lambda x: x.title if x.title else "")

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

    def add_entry(self):
        dialog = EntryDialog(self, title="New Entry")
        if dialog.exec():
            title, user, pwd, url, notes = dialog.get_data()
            if not title:
                QMessageBox.warning(self, "Error", "Title is required")
                return
                
            try:
                self.db.add_entry(title, user, pwd, url, notes)
                self.load_entries()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add entry: {e}")

    def edit_entry(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        uuid_str = self.table.item(row, 0).text()
        
        # PyKeePass lookup
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update entry: {e}")

    def delete_entry(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        uuid_str = self.table.item(row, 0).text()
        
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this entry?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            import uuid
            self.db.delete_entry(uuid.UUID(uuid_str))
            self.load_entries()

    def show_context_menu(self, position):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        menu.addSeparator()
        copy_user_action = menu.addAction("Copy Username")
        copy_pass_action = menu.addAction("Copy Password")
        
        action = menu.exec(self.table.viewport().mapToGlobal(position))
        
        if action == edit_action:
            self.edit_entry()
        elif action == delete_action:
            self.delete_entry()
        elif action == copy_user_action:
            self.copy_field(2) # Username column
        elif action == copy_pass_action:
            self.copy_password()

    def copy_field(self, col_index):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        text = self.table.item(row, col_index).text()
        QGuiApplication.clipboard().setText(text)

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

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.db.save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        close_vault_action = QAction("Close &Vault", self)
        close_vault_action.triggered.connect(self.logout)
        file_menu.addAction(close_vault_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")

        add_action = QAction("&Add Entry", self)
        add_action.setShortcut(QKeySequence.New)
        add_action.triggered.connect(self.add_entry)
        edit_menu.addAction(add_action)

        edit_entry_action = QAction("&Edit Entry", self)
        edit_entry_action.triggered.connect(self.edit_entry)
        edit_menu.addAction(edit_entry_action)
        
        delete_action = QAction("&Delete Entry", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self.delete_entry)
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        copy_user_action = QAction("Copy &Username", self)
        copy_user_action.triggered.connect(lambda: self.copy_field(2))
        edit_menu.addAction(copy_user_action)

        copy_pass_action = QAction("Copy &Password", self)
        copy_pass_action.triggered.connect(self.copy_password)
        edit_menu.addAction(copy_pass_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.information(self, "About Keyflow", 
                              "Keyflow Password Manager\n\n"
                              "A secure, open-source password manager supporting .kdbx files.\n"
                              "Built with Python and PySide6.")
