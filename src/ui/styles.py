
DARK_THEME = """
QWidget {
    background-color:
    color:
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Dialogs */
QDialog {
    background-color:
}

/* Inputs */
QLineEdit, QTextEdit {
    background-color:
    border: 1px solid
    border-radius: 6px;
    padding: 8px;
    color:
    selection-background-color:
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid
    background-color:
}

/* GroupBox/Labels */
QLabel {
    color:
    font-weight: 500;
}

/* List/Tree/Table */
QTableWidget, QTreeWidget, QListWidget {
    background-color:
    border: 1px solid
    gridline-color:
    selection-background-color:
    selection-color:
}

QHeaderView::section {
    background-color:
    padding: 6px;
    border: none;
    border-bottom: 1px solid
}

/* Buttons */
QPushButton {
    background-color:
    border: 1px solid
    border-radius: 6px;
    padding: 8px 16px;
    min-width: 80px;
}

QPushButton:hover {
    background-color:
}

QPushButton:pressed {
    background-color:
}

/* Primary Button Action */
QPushButton[role="primary"] {
    background-color:
    border: 1px solid
    color: white;
    font-weight: bold;
}

QPushButton[role="primary"]:hover {
    background-color:
}

/* Danger Button */
QPushButton[role="danger"] {
    background-color:
    border: 1px solid
}

/* Menu Bar */
QMenuBar {
    background-color:
    color:
}
QMenuBar::item {
    padding: 6px 10px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color:
}
QMenu {
    background-color:
    border: 1px solid
}
QMenu::item {
    padding: 6px 24px;
}
QMenu::item:selected {
    background-color:
}
"""
