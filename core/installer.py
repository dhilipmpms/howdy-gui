import subprocess
import os
from core.checks import get_distro, is_howdy_installed

SCRIPT_PATH = os.path.abspath("scripts/install_howdy.sh")

def install_howdy():
    distro = get_distro()

    if distro == "arch":
        return False, (
            "Arch Linux detected.\n\n"
            "Install Howdy from AUR:\n"
            "yay -S howdy"
        )

    cmd = ["bash", SCRIPT_PATH, distro]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return False, "Howdy installation failed."

    if is_howdy_installed():
        return True, "Howdy installed successfully."
    else:
        return False, "Howdy install finished but command not found."
