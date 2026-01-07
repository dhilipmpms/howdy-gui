from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QLineEdit, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from core.howdy import howdy_list, howdy_add, howdy_remove, howdy_clear


class ModelsTab(QWidget):
    """Tab for managing face models."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_models()
    
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Face Models")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # Model list
        self.model_list = QListWidget()
        self.model_list.setMinimumHeight(200)
        layout.addWidget(self.model_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("Add Model")
        self.btn_add.clicked.connect(self.add_model)
        btn_layout.addWidget(self.btn_add)
        
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.clicked.connect(self.remove_model)
        btn_layout.addWidget(self.btn_remove)
        
        self.btn_clear = QPushButton("Clear All")
        self.btn_clear.clicked.connect(self.clear_models)
        btn_layout.addWidget(self.btn_clear)
        
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.clicked.connect(self.refresh_models)
        btn_layout.addWidget(self.btn_refresh)
        
        layout.addLayout(btn_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def refresh_models(self):
        """Refresh the list of face models."""
        self.status_label.setText("Loading models...")
        self.model_list.clear()
        
        success, models, error = howdy_list()
        
        if success:
            if models:
                for model in models:
                    label = model['label']
                    model_id = model['id']
                    date = model['date']
                    display = f"ID: {model_id} | {label}"
                    if date:
                        display += f" | {date}"
                    
                    self.model_list.addItem(display)
                    # Store model ID in item data
                    item = self.model_list.item(self.model_list.count() - 1)
                    item.setData(Qt.ItemDataRole.UserRole, model_id)
                
                self.status_label.setText(f"{len(models)} model(s) found")
            else:
                self.model_list.addItem("No models found")
                self.status_label.setText("No models")
        else:
            self.model_list.addItem(f"Error: {error}")
            self.status_label.setText("Error loading models")
    
    def add_model(self):
        """Add a new face model."""
        label, ok = QInputDialog.getText(
            self,
            "Add Face Model",
            "Enter a label for this model (e.g., 'glasses', 'no-glasses'):"
        )
        
        if not ok or not label:
            return
        
        self.status_label.setText("Adding model... Look at the camera!")
        
        # Show instruction dialog
        QMessageBox.information(
            self,
            "Instructions",
            f"Adding model: {label}\\n\\n"
            "Look at the camera and follow the terminal instructions.\\n"
            "The camera window will open shortly."
        )
        
        success, message = howdy_add(label)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_models()
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("Failed to add model")
    
    def remove_model(self):
        """Remove the selected face model."""
        current_item = self.model_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a model to remove")
            return
        
        model_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        if not model_id:
            QMessageBox.warning(self, "Error", "Cannot determine model ID")
            return
        
        # Confirm removal
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove model ID {model_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.status_label.setText("Removing model...")
        success, message = howdy_remove(model_id)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_models()
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("Failed to remove model")
    
    def clear_models(self):
        """Clear all face models."""
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Are you sure you want to remove ALL face models?\\n\\n"
            "This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.status_label.setText("Clearing all models...")
        success, message = howdy_clear()
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_models()
        else:
            QMessageBox.warning(self, "Failed", message)
            self.status_label.setText("Failed to clear models")
