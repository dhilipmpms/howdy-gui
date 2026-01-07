from PyQt6.QtWidgets import QMessageBox
from core.installer import install_howdy

def setup_howdy(parent=None):
    reply = QMessageBox.question(
        parent,
        "Howdy not installed",
        "Howdy is not installed.\n\n"
        "Do you want to install it now?\n"
        "(You may be asked for your password)",
    )

    if reply.name != "Yes":
        return False

    ok, msg = install_howdy()

    if ok:
        QMessageBox.information(parent, "Success", msg)
        return True
    else:
        QMessageBox.critical(parent, "Error", msg)
        return False
