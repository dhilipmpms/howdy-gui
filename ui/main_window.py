from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel
)
from PyQt6.QtCore import Qt
from ui.models_tab import ModelsTab
from ui.config_tab import ConfigTab
from ui.test_tab import TestTab


class MainWindow(QWidget):
    """Main window with tabbed interface for Howdy management."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Howdy Face Authentication Manager")
        self.setMinimumSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Howdy Face Authentication Manager")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                padding: 10px 20px;
                margin: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # Add tabs
        self.models_tab = ModelsTab()
        self.config_tab = ConfigTab()
        self.test_tab = TestTab()
        
        self.tabs.addTab(self.models_tab, "📸 Face Models")
        self.tabs.addTab(self.config_tab, "⚙️ Configuration")
        self.tabs.addTab(self.test_tab, "🧪 Test")
        
        layout.addWidget(self.tabs)
        
        # Footer
        footer = QLabel("Manage face authentication for your system")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 10px; padding: 5px;")
        layout.addWidget(footer)
        
        self.setLayout(layout)
