from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QPushButton,
    QComboBox, QDoubleSpinBox, QSpinBox, QLabel, QMessageBox, QHBoxLayout
)
from core.config import read_howdy_config, write_howdy_config, get_available_cameras, validate_config


class ConfigTab(QWidget):
    """Tab for configuring Howdy settings."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Howdy Configuration")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # Form layout
        form = QFormLayout()
        
        # Camera device selection
        self.device_combo = QComboBox()
        self.device_combo.setMinimumWidth(200)
        form.addRow("Camera Device:", self.device_combo)
        
        # Certainty threshold
        self.certainty_spin = QDoubleSpinBox()
        self.certainty_spin.setRange(0.0, 10.0)
        self.certainty_spin.setSingleStep(0.1)
        self.certainty_spin.setDecimals(1)
        self.certainty_spin.setSuffix(" (lower = stricter)")
        certainty_help = QLabel("How certain the system needs to be (3.5 recommended)")
        certainty_help.setStyleSheet("color: gray; font-size: 10px;")
        form.addRow("Certainty:", self.certainty_spin)
        form.addRow("", certainty_help)
        
        # Timeout
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 60)
        self.timeout_spin.setSuffix(" seconds")
        timeout_help = QLabel("How long to wait for face detection")
        timeout_help.setStyleSheet("color: gray; font-size: 10px;")
        form.addRow("Timeout:", self.timeout_spin)
        form.addRow("", timeout_help)
        
        # Dark threshold
        self.dark_threshold_spin = QDoubleSpinBox()
        self.dark_threshold_spin.setRange(0.0, 100.0)
        self.dark_threshold_spin.setSingleStep(1.0)
        self.dark_threshold_spin.setDecimals(1)
        dark_help = QLabel("Minimum brightness level for detection")
        dark_help.setStyleSheet("color: gray; font-size: 10px;")
        form.addRow("Dark Threshold:", self.dark_threshold_spin)
        form.addRow("", dark_help)
        
        layout.addLayout(form)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("Save Configuration")
        self.btn_save.clicked.connect(self.save_config)
        btn_layout.addWidget(self.btn_save)
        
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_reset.clicked.connect(self.reset_config)
        btn_layout.addWidget(self.btn_reset)
        
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.load_config)
        btn_layout.addWidget(self.btn_refresh)
        
        layout.addLayout(btn_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
        
        # Info section
        info = QLabel(
            "⚠️ Note: Changing these settings requires sudo privileges.\\n"
            "You may be prompted for your password."
        )
        info.setStyleSheet("color: orange; font-size: 10px; margin-top: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_config(self):
        """Load current configuration."""
        self.status_label.setText("Loading configuration...")
        
        # Load available cameras
        cameras = get_available_cameras()
        self.device_combo.clear()
        
        if cameras:
            self.device_combo.addItems(cameras)
        else:
            self.device_combo.addItem("/dev/video0")
            self.status_label.setText("Warning: No cameras detected")
        
        # Load config settings
        config = read_howdy_config()
        
        if config:
            # Set device
            device_path = config.get('device_path', '/dev/video0')
            index = self.device_combo.findText(device_path)
            if index >= 0:
                self.device_combo.setCurrentIndex(index)
            
            # Set other values
            self.certainty_spin.setValue(config.get('certainty', 3.5))
            self.timeout_spin.setValue(config.get('timeout', 5))
            self.dark_threshold_spin.setValue(config.get('dark_threshold', 50.0))
            
            self.status_label.setText("Configuration loaded")
        else:
            self.status_label.setText("Warning: Could not read config file")
            # Set defaults
            self.certainty_spin.setValue(3.5)
            self.timeout_spin.setValue(5)
            self.dark_threshold_spin.setValue(50.0)
    
    def save_config(self):
        """Save configuration changes."""
        settings = {
            'device_path': self.device_combo.currentText(),
            'certainty': self.certainty_spin.value(),
            'timeout': self.timeout_spin.value(),
            'dark_threshold': self.dark_threshold_spin.value(),
        }
        
        # Validate settings
        valid, errors = validate_config(settings)
        
        if not valid:
            QMessageBox.warning(
                self,
                "Invalid Configuration",
                "Configuration errors:\\n" + "\\n".join(errors)
            )
            return
        
        self.status_label.setText("Saving configuration...")
        
        success, message = write_howdy_config(settings)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.status_label.setText("Configuration saved")
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("Failed to save configuration")
    
    def reset_config(self):
        """Reset to default values."""
        reply = QMessageBox.question(
            self,
            "Reset Configuration",
            "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.certainty_spin.setValue(3.5)
            self.timeout_spin.setValue(5)
            self.dark_threshold_spin.setValue(50.0)
            self.status_label.setText("Reset to defaults (not saved)")
