from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from core.howdy import howdy_test


class TestTab(QWidget):
    """Tab for testing face recognition."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Test Face Recognition")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # Instructions
        instructions = QLabel(
            "Click the button below to test face recognition.\\n"
            "Make sure you have at least one face model added.\\n"
            "Look at the camera when prompted."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray; margin: 10px 0;")
        layout.addWidget(instructions)
        
        # Test button
        self.btn_test = QPushButton("Test Face Recognition")
        self.btn_test.setMinimumHeight(50)
        self.btn_test.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_test.clicked.connect(self.run_test)
        layout.addWidget(self.btn_test)
        
        # Result display
        result_label = QLabel("Test Results:")
        result_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(150)
        self.result_text.setPlaceholderText("Test results will appear here...")
        layout.addWidget(self.result_text)
        
        # Status label
        self.status_label = QLabel("Ready to test")
        self.status_label.setStyleSheet("color: gray; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def run_test(self):
        """Run face recognition test."""
        self.status_label.setText("🔍 Testing... Look at the camera!")
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        self.result_text.clear()
        self.btn_test.setEnabled(False)
        
        # Show info dialog
        QMessageBox.information(
            self,
            "Testing Face Recognition",
            "The camera will activate now.\\n\\n"
            "Look directly at the camera and wait for the result.\\n"
            "This may take a few seconds."
        )
        
        # Run test
        success, message = howdy_test()
        
        # Update UI with results
        if success:
            self.result_text.setStyleSheet("color: green; font-weight: bold;")
            self.result_text.setText(f"✅ SUCCESS\\n\\n{message}")
            self.status_label.setText("✅ Face recognized!")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            
            QMessageBox.information(
                self,
                "Test Successful",
                "Face recognized successfully!\\n\\n"
                "Your face authentication is working correctly."
            )
        else:
            self.result_text.setStyleSheet("color: red;")
            self.result_text.setText(f"❌ FAILED\\n\\n{message}")
            self.status_label.setText("❌ Face not recognized")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            
            QMessageBox.warning(
                self,
                "Test Failed",
                f"Face recognition failed.\\n\\n{message}\\n\\n"
                "Make sure you have added at least one face model."
            )
        
        self.btn_test.setEnabled(True)
