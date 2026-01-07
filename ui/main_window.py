from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel,
    QVBoxLayout, QMessageBox
)
from core.howdy import howdy_test, howdy_add

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Howdy Face Authentication")

        self.status = QLabel("Status: Ready")

        self.btn_test = QPushButton("Test Face")
        self.btn_add = QPushButton("Add Face")

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.btn_test)
        layout.addWidget(self.btn_add)
        self.setLayout(layout)

        self.btn_test.clicked.connect(self.run_test)
        self.btn_add.clicked.connect(self.run_add)

    def run_test(self):
        self.status.setText("Testing face...")
        result = howdy_test()

        if result.returncode == 0:
            QMessageBox.information(self, "Success", "Face recognized")
            self.status.setText("Status: Success")
        else:
            QMessageBox.warning(self, "Failed", "Face not recognized")
            self.status.setText("Status: Failed")

    def run_add(self):
        QMessageBox.information(
            self,
            "Instructions",
            "Look at the camera.\nFollow terminal instructions."
        )

        result = howdy_add()
        if result.returncode == 0:
            QMessageBox.information(self, "Done", "Face added successfully")
        else:
            QMessageBox.warning(self, "Failed", "Could not add face")
