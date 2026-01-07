import distro
import shutil

def get_distro():
    return distro.id().lower()

def is_howdy_installed():
    return shutil.which("howdy") is not None
