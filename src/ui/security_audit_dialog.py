import string
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, 
                               QPushButton, QHBoxLayout, QTabWidget, QWidget, QHeaderView)
from PySide6.QtGui import QColor

class SecurityAuditDialog(QDialog):
    def __init__(self, entries, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Auditoría de Seguridad")
        self.resize(700, 500)
        
        self.entries = entries
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        title = QLabel("Informe de Seguridad")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #007acc;")
        layout.addWidget(title)
        
        description = QLabel("Hemos analizado tus contraseñas para encontrar vulnerabilidades potenciales.")
        description.setStyleSheet("color: #aaaaaa; margin-bottom: 10px;")
        layout.addWidget(description)
        
        # Tabs for different issues
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #3d3d3d; border-radius: 4px; }
            QTabBar::tab { background: #2d2d2d; color: #aaa; padding: 8px 12px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #3d3d3d; color: white; border-bottom: 2px solid #007acc; }
        """)
        
        # Tab 1: Duplicated Passwords
        self.duplicates_tab = QWidget()
        self.setup_duplicates_tab()
        self.tabs.addTab(self.duplicates_tab, "⚠️ Contraseñas Duplicadas")
        
        # Tab 2: Weak Passwords
        self.weak_tab = QWidget()
        self.setup_weak_tab()
        self.tabs.addTab(self.weak_tab, "🔓 Contraseñas Débiles")
        
        layout.addWidget(self.tabs)
        
        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def setup_duplicates_tab(self):
        layout = QVBoxLayout(self.duplicates_tab)
        
        info = QLabel("Las siguientes entradas comparten la misma contraseña. Si una se ve comprometida, todas lo estarán.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #e0e0e0; margin: 10px 0;")
        layout.addWidget(info)
        
        tree = QTreeWidget()
        tree.setHeaderLabels(["Título", "Usuario", "Ubicación"])
        tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tree.setIndentation(20)
        
        # Analyze duplicates
        password_map = {}
        for entry in self.entries:
            if not entry.password:
                continue
            if entry.password not in password_map:
                password_map[entry.password] = []
            password_map[entry.password].append(entry)
            
        duplicates = {p: es for p, es in password_map.items() if len(es) > 1}
        
        if not duplicates:
            layout.addWidget(QLabel("¡Genial! No tienes contraseñas duplicadas."))
            tree.hide()
        else:
            for pwd, entries in duplicates.items():
                # Mask password for the group title
                masked_pwd = "••••" + pwd[-2:] if len(pwd) > 2 else "••••"
                group = QTreeWidgetItem(tree)
                group.setText(0, f"Contraseña: {masked_pwd} ({len(entries)} entradas)")
                group.setForeground(0, QColor("#ff6b6b"))
                group.setExpanded(True)
                
                for entry in entries:
                    item = QTreeWidgetItem(group)
                    item.setText(0, entry.title or "(Sin título)")
                    item.setText(1, entry.username or "")
                    item.setText(2, entry.url or "")
                    
            layout.addWidget(tree)

    def setup_weak_tab(self):
        layout = QVBoxLayout(self.weak_tab)
        
        info = QLabel("Estas contraseñas son fáciles de adivinar por fuerza bruta. Se recomienda que tengan al menos 12 caracteres, mayúsculas, números y símbolos.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #e0e0e0; margin: 10px 0;")
        layout.addWidget(info)
        
        tree = QTreeWidget()
        tree.setHeaderLabels(["Título", "Problema Detectado", "Longitud"])
        tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        weak_entries = []
        for entry in self.entries:
            if not entry.password:
                continue
            
            pwd = entry.password
            issues = []
            
            if len(pwd) < 8:
                issues.append("Muy corta (< 8 letras)")
            elif len(pwd) < 12:
                issues.append("Corta (< 12 letras)")
                
            has_upper = any(c in string.ascii_uppercase for c in pwd)
            has_lower = any(c in string.ascii_lowercase for c in pwd)
            has_digit = any(c in string.digits for c in pwd)
            has_special = any(c in string.punctuation for c in pwd)
            
            missing = []
            if not has_upper: missing.append("Mayúsculas")
            if not has_lower: missing.append("Minúsculas")
            if not has_digit: missing.append("Números")
            if not has_special: missing.append("Símbolos")
            
            if missing:
                issues.append(f"Falta: {', '.join(missing)}")
                
            if issues:
                weak_entries.append((entry, ", ".join(issues)))
        
        if not weak_entries:
            layout.addWidget(QLabel("¡Excelente! Todas tus contraseñas parecen fuertes."))
            tree.hide()
        else:
            for entry, issue in weak_entries:
                item = QTreeWidgetItem(tree)
                item.setText(0, entry.title or "(Sin título)")
                item.setText(1, issue)
                item.setText(2, str(len(entry.password)))
                
                # Color coding based on severity
                if "Muy corta" in issue:
                    item.setForeground(1, QColor("#ff6b6b")) # Red
                else:
                    item.setForeground(1, QColor("#ffb74d")) # Orange
                    
            layout.addWidget(tree)
