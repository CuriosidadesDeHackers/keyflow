from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QPushButton, QWidget, QGridLayout, QScrollArea)
from PySide6.QtCore import Qt
import secrets
import string

class EntryDialog(QDialog):
    def __init__(self, parent=None, title="", username="", password="", url="", notes="", emoji=""):
        super().__init__(parent)
        self.setWindowTitle("Detalles de la Entrada")
        
        self.setModal(True)
        self.resize(500, 700)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel(title or "Detalles de la Entrada")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        # Título y Emoji en la misma fila
        title_emoji_layout = QHBoxLayout()
        
        title_container = QWidget()
        title_v_layout = QVBoxLayout(title_container)
        title_v_layout.setContentsMargins(0, 0, 0, 0)
        title_v_layout.setSpacing(4)
        title_v_layout.addWidget(QLabel("Título"))
        self.title_input = QLineEdit(title)
        self.title_input.setPlaceholderText("ej. Cuenta de Google")
        title_v_layout.addWidget(self.title_input)
        
        emoji_container = QWidget()
        emoji_v_layout = QVBoxLayout(emoji_container)
        emoji_v_layout.setContentsMargins(0, 0, 0, 0)
        emoji_v_layout.setSpacing(4)
        emoji_v_layout.addWidget(QLabel("Emoji"))
        self.emoji_input = QLineEdit(emoji)
        self.emoji_input.setPlaceholderText("😀")
        self.emoji_input.setMaxLength(2)
        self.emoji_input.setFixedWidth(70)
        self.emoji_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_input.setStyleSheet("font-size: 24px;")
        emoji_v_layout.addWidget(self.emoji_input)
        
        title_emoji_layout.addWidget(title_container)
        title_emoji_layout.addWidget(emoji_container)
        form_layout.addLayout(title_emoji_layout)
        
        # Catálogo de emojis
        emoji_catalog_label = QLabel("Selecciona un emoji:")
        emoji_catalog_label.setStyleSheet("font-size: 12px; color: #888; margin-top: 5px;")
        form_layout.addWidget(emoji_catalog_label)
        
        # Grid de emojis predefinidos
        emoji_grid = QGridLayout()
        emoji_grid.setSpacing(4)
        
        # Catálogo de emojis comunes organizados por categorías
        self.emoji_catalog = [
            # Seguridad y Claves
            "🔑", "🔐", "🔒", "🔓", "🛡️",
            # Comunicación
            "📧", "✉️", "📨", "💬", "📱",
            # Finanzas
            "💳", "💰", "🏦", "💵", "💴",
            # Tecnología
            "💻", "🖥️", "⌨️", "🖱️", "📡",
            # Internet y Web
            "🌐", "🌍", "🔗", "📶", "🛜",
            # Trabajo y Productividad
            "💼", "📊", "📈", "📋", "✏️",
            # Entretenimiento
            "🎮", "🎯", "🎬", "🎵", "📺",
            # Social
            "👤", "👥", "🙋", "💭", "❤️",
            # Cloud y Almacenamiento
            "☁️", "💾", "📁", "📂", "🗂️",
            # Shopping y Comercio
            "🛒", "🛍️", "🏪", "🏬", "💸",
            # Diversos
            "⭐", "✨", "🔔", "📌", "🏠",
        ]
        
        # Crear botones para cada emoji
        row, col = 0, 0
        for emoji_char in self.emoji_catalog:
            btn = QPushButton(emoji_char)
            btn.setFixedSize(38, 38)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #2b2b2b;
                }
                QPushButton:hover {
                    background-color: #3b3b3b;
                    border-color: #777;
                }
                QPushButton:pressed {
                    background-color: #1b1b1b;
                }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, e=emoji_char: self.select_emoji(e))
            emoji_grid.addWidget(btn, row, col)
            
            col += 1
            if col >= 10:  # 10 emojis por fila
                col = 0
                row += 1
        
        # Contenedor con scroll para el catálogo
        emoji_widget = QWidget()
        emoji_widget.setLayout(emoji_grid)
        
        scroll = QScrollArea()
        scroll.setWidget(emoji_widget)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(200)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                border-radius: 4px;
                background-color: #1e1e1e;
            }
        """)
        
        form_layout.addWidget(scroll)
        
        form_layout.addWidget(QLabel("Usuario"))
        self.user_input = QLineEdit(username)
        self.user_input.setPlaceholderText("email@example.com")
        form_layout.addWidget(self.user_input)
        
        form_layout.addWidget(QLabel("Contraseña"))
        pass_layout = QHBoxLayout()
        self.pass_input = QLineEdit(password)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("••••••••")
        
        self.toggle_btn = QPushButton("Mostrar")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedWidth(80)
        self.toggle_btn.clicked.connect(self.toggle_password)
        
        self.gen_btn = QPushButton("Generar")
        self.gen_btn.setFixedWidth(100)
        self.gen_btn.setProperty("class", "primary")
        self.gen_btn.clicked.connect(self.generate_password)
        
        pass_layout.addWidget(self.pass_input)
        pass_layout.addWidget(self.toggle_btn)
        pass_layout.addWidget(self.gen_btn)
        form_layout.addLayout(pass_layout)

        form_layout.addWidget(QLabel("URL"))
        self.url_input = QLineEdit(url)
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addWidget(self.url_input)
        
        form_layout.addWidget(QLabel("Notes"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(notes)
        self.notes_input.setPlaceholderText("Additional details...")
        self.notes_input.setFixedHeight(120)
        form_layout.addWidget(self.notes_input)
        
        layout.addLayout(form_layout)
        
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Guardar")
        self.save_btn.setProperty("role", "primary")
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)

    def toggle_password(self, checked):
        if checked:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Ocultar")
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("Mostrar")
    
    def select_emoji(self, emoji):
        """Selecciona un emoji del catálogo"""
        self.emoji_input.setText(emoji)

    def generate_password(self):
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        
        self.pass_input.setText(password)
        
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.setText("Ocultar")

    def get_data(self):
        return (
            self.title_input.text(),
            self.user_input.text(),
            self.pass_input.text(),
            self.url_input.text(),
            self.notes_input.toPlainText(),
            self.emoji_input.text().strip()  # Emoji como sexto elemento
        )
