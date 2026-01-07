import distro
import shutil

def get_distro():
    """Get the distribution ID (lowercase)."""
    return distro.id().lower()

def get_distro_info():
    """
    Get detailed distribution information.
    
    Returns:
        dict: Contains 'id', 'version', 'name', and 'family' keys
    """
    distro_id = distro.id().lower()
    version = distro.version()
    name = distro.name()
    
    # Determine distro family
    family = "unknown"
    if distro_id in ["ubuntu", "debian", "pop", "linuxmint", "elementary", "zorin"]:
        family = "debian"
    elif distro_id in ["fedora", "rhel", "centos", "rocky", "almalinux"]:
        family = "fedora"
    elif distro_id in ["arch", "manjaro", "endeavouros", "garuda"]:
        family = "arch"
    
    return {
        "id": distro_id,
        "version": version,
        "name": name,
        "family": family
    }

def is_howdy_installed():
    """Check if Howdy is installed on the system."""
    return shutil.which("howdy") is not None
