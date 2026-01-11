DARK_THEME = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QPushButton {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
    min-height: 28px;
}

QPushButton:hover {
    background-color: #3a3a3a;
    border: 1px solid #4a4a4a;
}

QPushButton:pressed {
    background-color: #252525;
}

QPushButton:disabled {
    background-color: #2d2d2d;
    color: #666666;
    border: 1px solid #333333;
}

QPushButton[class="primary"] {
    background-color: #007acc;
    color: white;
    border: 1px solid #005a9e;
}

QPushButton[class="primary"]:hover {
    background-color: #1a8cdb;
    border: 1px solid #006bb3;
}

QPushButton[class="primary"]:pressed {
    background-color: #005a9e;
}

QPushButton[class="danger"] {
    background-color: #d32f2f;
    color: white;
    border: 1px solid #b71c1c;
}

QPushButton[class="danger"]:hover {
    background-color: #e74c3c;
    border: 1px solid #c62828;
}

QPushButton[class="danger"]:pressed {
    background-color: #b71c1c;
}

QPushButton[class="secondary"] {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    color: #b0b0b0;
}

QPushButton[class="secondary"]:hover {
    background-color: #3a3a3a;
    border: 1px solid #4a4a4a;
    color: #e0e0e0;
}

QLineEdit, QTextEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 3px;
    padding: 6px 10px;
    selection-background-color: #007acc;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #007acc;
    background-color: #323232;
}

QLineEdit::placeholder {
    color: #666666;
}

QTableWidget {
    background-color: #252525;
    alternate-background-color: #2a2a2a;
    gridline-color: #333333;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
    selection-background-color: #0e639c;
}

QTableWidget::item {
    padding: 6px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #0e639c;
    color: white;
}

QHeaderView::section {
    background-color: #2d2d2d;
    color: #b0b0b0;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #404040;
    font-weight: 600;
}

QMenuBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border-bottom: 1px solid #3d3d3d;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 12px;
    border-radius: 3px;
}

QMenuBar::item:selected {
    background-color: #007acc;
}

QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
}

QMenu::item {
    padding: 6px 20px;
    border-radius: 2px;
}

QMenu::item:selected {
    background-color: #007acc;
}

QMenu::separator {
    height: 1px;
    background-color: #3d3d3d;
    margin: 3px 0px;
}

QDialog {
    background-color: #1e1e1e;
    border: 1px solid #3d3d3d;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #888888;
    border-top: 1px solid #3d3d3d;
}
"""
