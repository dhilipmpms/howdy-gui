import subprocess
import os
from core.checks import get_distro_info, is_howdy_installed

SCRIPT_PATH = os.path.abspath("scripts/install_howdy.sh")

def install_howdy():
    """
    Install Howdy based on the detected distribution.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    distro_info = get_distro_info()
    distro_id = distro_info["id"]
    version = distro_info["version"]
    family = distro_info["family"]
    
    # Ubuntu 24.04+ uses a different PPA and requires additional setup
    ubuntu_24_plus = distro_id == "ubuntu" and version and (
        version.startswith("24") or version.startswith("25")
    )
    
    # Handle Arch-based distributions
    if family == "arch":
        return False, (
            f"{distro_info['name']} detected.\\n\\n"
            "Install Howdy from AUR:\\n"
            "  yay -S howdy\\n"
            "or\\n"
            "  paru -S howdy\\n\\n"
            "After installation, restart this application."
        )
    
    # Handle unsupported distributions
    if family == "unknown":
        return False, (
            f"Unsupported distribution: {distro_info['name']}\\n\\n"
            "Howdy installation is only supported on:\\n"
            "- Debian/Ubuntu-based distributions\\n"
            "- Fedora/RHEL-based distributions\\n"
            "- Arch-based distributions (via AUR)\\n\\n"
            "Please install Howdy manually for your distribution."
        )
    
    # Run installation script
    cmd = ["bash", SCRIPT_PATH, distro_id, version, family, str(ubuntu_24_plus).lower()]
    
    try:
        result = subprocess.run(
            cmd, 
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else e.stdout
        return False, (
            f"Howdy installation failed.\\n\\n"
            f"Error: {error_msg}\\n\\n"
            f"Distribution: {distro_info['name']} {version}"
        )
    
    # Verify installation
    if is_howdy_installed():
        success_msg = f"Howdy installed successfully on {distro_info['name']} {version}!\\n\\n"
        
        if ubuntu_24_plus:
            success_msg += (
                "✅ Ubuntu 24.04+ installation complete!\\n\\n"
                "Note: This version uses the unofficial PPA (ppa:ubuntuhandbook1/howdy) "
                "with additional Python dependencies.\\n\\n"
            )
        
        success_msg += "You can now configure and use face authentication."
        
        return True, success_msg
    else:
        return False, (
            "Installation script completed but Howdy command not found.\\n\\n"
            "Please check your system logs or try installing manually."
        )
