
DARK_THEME = """
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Dialogs */
QDialog {
    background-color: #252526;
}

/* Inputs */
QLineEdit, QTextEdit {
    background-color: #333333;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 8px;
    color: #ffffff;
    selection-background-color: #264f78;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #007acc;
    background-color: #3c3c3c;
}

/* GroupBox/Labels */
QLabel {
    color: #cccccc;
    font-weight: 500;
}

/* List/Tree/Table */
QTableWidget, QTreeWidget, QListWidget {
    background-color: #252526;
    border: 1px solid #3e3e42;
    gridline-color: #3e3e42;
    selection-background-color: #37373d;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #333333;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #3e3e42;
}

/* Buttons */
QPushButton {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 8px 16px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #4a4a4a;
}

QPushButton:pressed {
    background-color: #2d2d2d;
}

/* Primary Button Action */
QPushButton[role="primary"] {
    background-color: #0e639c;
    border: 1px solid #0e639c;
    color: white;
    font-weight: bold;
}

QPushButton[role="primary"]:hover {
    background-color: #1177bb;
}

/* Danger Button */
QPushButton[role="danger"] {
    background-color: #ce3131;
    border: 1px solid #ce3131;
}

/* Menu Bar */
QMenuBar {
    background-color: #333333;
    color: #ffffff;
}
QMenuBar::item {
    padding: 6px 10px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color: #4a4a4a;
}
QMenu {
    background-color: #252526;
    border: 1px solid #454545;
}
QMenu::item {
    padding: 6px 24px;
}
QMenu::item:selected {
    background-color: #37373d;
}
"""
