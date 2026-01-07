import subprocess
import shutil

def is_howdy_installed():
    return shutil.which("howdy") is not None


def howdy_test():
    # MANUAL ONLY – opens camera once
    return subprocess.run(
        ["howdy", "test"],
        timeout=30
    )


def howdy_add():
    # MANUAL ONLY – must be user session
    return subprocess.run(
        ["howdy", "add"],
        timeout=120
    )
