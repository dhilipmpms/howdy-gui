import configparser
import os
import subprocess
import re

# Howdy config path
HOWDY_CONFIG_PATH = "/lib/security/howdy/config.ini"

def read_howdy_config():
    """
    Read Howdy configuration file.
    
    Returns:
        dict: Configuration settings or None if error
    """
    try:
        if not os.path.exists(HOWDY_CONFIG_PATH):
            return None
        
        config = configparser.ConfigParser()
        config.read(HOWDY_CONFIG_PATH)
        
        # Extract key settings
        settings = {
            'device_path': config.get('video', 'device_path', fallback='/dev/video0'),
            'certainty': config.getfloat('video', 'certainty', fallback=3.5),
            'timeout': config.getint('video', 'timeout', fallback=5),
            'dark_threshold': config.getfloat('video', 'dark_threshold', fallback=50.0),
            'video_certainty': config.getfloat('video', 'video_certainty', fallback=2.5),
        }
        
        return settings
        
    except Exception as e:
        print(f"Error reading config: {e}")
        return None


def write_howdy_config(settings):
    """
    Write Howdy configuration file.
    
    Args:
        settings: dict with configuration values
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if not os.path.exists(HOWDY_CONFIG_PATH):
            return False, "Config file not found"
        
        config = configparser.ConfigParser()
        config.read(HOWDY_CONFIG_PATH)
        
        # Update settings
        if 'device_path' in settings:
            config.set('video', 'device_path', str(settings['device_path']))
        
        if 'certainty' in settings:
            config.set('video', 'certainty', str(settings['certainty']))
        
        if 'timeout' in settings:
            config.set('video', 'timeout', str(settings['timeout']))
        
        if 'dark_threshold' in settings:
            config.set('video', 'dark_threshold', str(settings['dark_threshold']))
        
        if 'video_certainty' in settings:
            config.set('video', 'video_certainty', str(settings['video_certainty']))
        
        # Write to temp file first, then use sudo to move
        temp_path = "/tmp/howdy_config.ini"
        with open(temp_path, 'w') as f:
            config.write(f)
        
        # Use sudo to copy to system location
        result = subprocess.run(
            ['sudo', 'cp', temp_path, HOWDY_CONFIG_PATH],
            capture_output=True,
            text=True
        )
        
        # Clean up temp file
        os.remove(temp_path)
        
        if result.returncode == 0:
            return True, "Configuration saved successfully"
        else:
            return False, f"Failed to save config: {result.stderr}"
            
    except Exception as e:
        return False, f"Error writing config: {str(e)}"


def get_available_cameras():
    """
    Detect available video devices (cameras).
    
    Returns:
        list: List of device paths
    """
    devices = []
    
    # Check /dev/video* devices
    for i in range(10):
        device = f"/dev/video{i}"
        if os.path.exists(device):
            devices.append(device)
    
    return devices


def validate_config(settings):
    """
    Validate configuration settings.
    
    Args:
        settings: dict with configuration values
        
    Returns:
        tuple: (valid: bool, errors: list)
    """
    errors = []
    
    # Validate certainty (lower = more strict)
    if 'certainty' in settings:
        certainty = settings['certainty']
        if not (0.0 <= certainty <= 10.0):
            errors.append("Certainty must be between 0.0 and 10.0")
    
    # Validate timeout
    if 'timeout' in settings:
        timeout = settings['timeout']
        if not (1 <= timeout <= 60):
            errors.append("Timeout must be between 1 and 60 seconds")
    
    # Validate device path
    if 'device_path' in settings:
        device = settings['device_path']
        if not os.path.exists(device):
            errors.append(f"Device {device} does not exist")
    
    return len(errors) == 0, errors
