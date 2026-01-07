import subprocess
import shutil
import re
import os

def get_actual_user():
    """
    Get the actual user, even when running with sudo/pkexec.
    
    Returns:
        str: The username of the actual user
    """
    # Try SUDO_USER first (set when using sudo)
    user = os.environ.get('SUDO_USER')
    if user:
        return user
    
    # Try PKEXEC_UID (set when using pkexec)
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if pkexec_uid:
        try:
            import pwd
            return pwd.getpwuid(int(pkexec_uid)).pw_name
        except:
            pass
    
    # Fall back to current user
    return os.environ.get('USER', 'root')

def is_howdy_installed():
    """Check if Howdy is installed on the system."""
    return shutil.which("howdy") is not None


def howdy_list():
    """
    List all face models for the current user.
    
    Returns:
        tuple: (success: bool, models: list of dict, error: str)
    """
    try:
        result = subprocess.run(
            ["howdy", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, [], result.stderr or "Failed to list models"
        
        # Parse the output to extract model information
        models = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            # Look for lines with model IDs (usually numeric)
            # Format is typically: ID  Label  Date
            match = re.match(r'^\s*(\d+)\s+(.+?)\s+(\d{4}-\d{2}-\d{2}.*)?$', line)
            if match:
                models.append({
                    'id': match.group(1),
                    'label': match.group(2).strip(),
                    'date': match.group(3).strip() if match.group(3) else ''
                })
        
        return True, models, ""
        
    except subprocess.TimeoutExpired:
        return False, [], "Command timed out"
    except Exception as e:
        return False, [], str(e)


def howdy_test():
    """
    Test face recognition.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        result = subprocess.run(
            ["howdy", "test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, "Face recognized successfully!"
        else:
            error_msg = result.stderr or result.stdout or "Face not recognized"
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Test timed out - no face detected"
    except Exception as e:
        return False, f"Error: {str(e)}"


def howdy_add(label=None, username=None):
    """
    Add a new face model.
    
    Args:
        label: Optional label for the model
        username: Optional username to add the model for (defaults to actual user)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get the actual user if not specified
        if username is None:
            username = get_actual_user()
        
        # Build command: howdy add <username> [label]
        cmd = ["howdy", "add", username]
        if label:
            cmd.append(label)
        
        # Run interactively - user needs to see camera feed
        result = subprocess.run(
            cmd,
            timeout=120
        )
        
        if result.returncode == 0:
            return True, f"Face model '{label or 'default'}' added successfully for user {username}!"
        else:
            return False, "Failed to add face model"
            
    except subprocess.TimeoutExpired:
        return False, "Add operation timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"


def howdy_remove(model_id):
    """
    Remove a face model by ID.
    
    Args:
        model_id: The ID of the model to remove
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        result = subprocess.run(
            ["howdy", "remove", str(model_id)],
            capture_output=True,
            text=True,
            timeout=10,
            input="y\n"  # Auto-confirm removal
        )
        
        if result.returncode == 0:
            return True, f"Model {model_id} removed successfully"
        else:
            error_msg = result.stderr or result.stdout or "Failed to remove model"
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Remove operation timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"


def howdy_clear():
    """
    Remove all face models for the current user.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        result = subprocess.run(
            ["howdy", "clear"],
            capture_output=True,
            text=True,
            timeout=10,
            input="y\n"  # Auto-confirm clear
        )
        
        if result.returncode == 0:
            return True, "All models cleared successfully"
        else:
            error_msg = result.stderr or result.stdout or "Failed to clear models"
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Clear operation timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"
