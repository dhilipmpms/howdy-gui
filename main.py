import sys
from PyQt6.QtWidgets import QApplication
from core.checks import is_howdy_installed
from ui.setup_dialog import setup_howdy
from ui.main_window import MainWindow

app = QApplication(sys.argv)

if not is_howdy_installed():
    installed = setup_howdy()
    if not installed:
        sys.exit(0)

window = MainWindow()
window.show()

sys.exit(app.exec())
