"""
Face model manager for Howdy GUI Manager
Handles face model operations (list, add, remove)
"""

import json
import os
import subprocess
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class ModelManager:
    """Manages Howdy face models"""
    
    def __init__(self, models_dir: str = "/lib/security/howdy/models"):
        self.models_dir = models_dir
    
    def is_root(self) -> bool:
        """Check if the process is running as root"""
        return os.getuid() == 0
    
    def get_base_cmd(self, use_sudo: bool = False) -> List[str]:
        """Get the base howdy command with optional elevation"""
        if self.is_root():
            return ['howdy']
        
        # Check for pkexec as it's better for GUI apps
        if os.path.exists('/usr/bin/pkexec'):
            return ['pkexec', 'howdy']
        
        return ['sudo', 'howdy']
    
    def get_user_models(self, username: str) -> List[Dict]:
        """Get all face models for a user"""
        model_file = os.path.join(self.models_dir, f"{username}.dat")
        
        if not os.path.exists(model_file):
            return []
        
        try:
            with open(model_file, 'r') as f:
                models = json.load(f)
                return models
        except Exception as e:
            print(f"Error loading models: {e}")
            return []
    
    def add_model(self, username: str, label: str = None) -> Tuple[bool, str]:
        """
        Add a new face model for a user
        Returns: (success, message)
        """
        try:
            base_cmd = self.get_base_cmd()
            cmd = base_cmd + ['-U', username, 'add']
            if label:
                cmd.append(label)
            
            # For 'add', we might want to run it in a way that respects the terminal
            # or captures output more gracefully if it's slow.
            # We use a longer timeout because face enrollment takes time.
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, "Face model added successfully"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                if "run this command as root" in error_msg:
                    return False, "Permission denied: Howdy must be run as root. Please start the app with sudo or ensure pkexec is working."
                return False, f"Error: {error_msg}"
        except subprocess.TimeoutExpired:
            return False, "Timeout: Face detection took too long. Make sure your camera is working and you are in a well-lit area."
        except Exception as e:
            return False, f"Error adding model: {str(e)}"
    
    def remove_model(self, username: str, model_id: int) -> Tuple[bool, str]:
        """
        Remove a face model
        Returns: (success, message)
        """
        try:
            base_cmd = self.get_base_cmd()
            cmd = base_cmd + ['-U', username, '-y', 'remove', str(model_id)]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "Face model removed successfully"
            else:
                return False, f"Error: {result.stderr or result.stdout}"
        except Exception as e:
            return False, f"Error removing model: {str(e)}"
    
    def clear_models(self, username: str) -> Tuple[bool, str]:
        """
        Clear all face models for a user
        Returns: (success, message)
        """
        try:
            base_cmd = self.get_base_cmd()
            cmd = base_cmd + ['-U', username, '-y', 'clear']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "All face models cleared"
            else:
                return False, f"Error: {result.stderr or result.stdout}"
        except Exception as e:
            return False, f"Error clearing models: {str(e)}"
    
    def test_recognition(self, username: str) -> Tuple[bool, str]:
        """
        Test face recognition
        Returns: (success, message)
        """
        try:
            base_cmd = self.get_base_cmd()
            cmd = base_cmd + ['-U', username, 'test']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                stdout_msg = result.stdout.strip() if result.stdout else ""
                return True, f"✓ Face recognized successfully!\n{stdout_msg}"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                return False, f"✗ Face not recognized.\nDetails: {error_msg}"
        except subprocess.TimeoutExpired:
            return False, "⏱ Timeout: Recognition test took too long. Make sure your camera is working."
        except Exception as e:
            return False, f"❌ Error testing recognition: {str(e)}"
    
    def test_recognition_detailed(self, username: str) -> Tuple[bool, str, Dict]:
        """
        Test face recognition with detailed output
        Returns: (success, message, details)
        """
        try:
            base_cmd = self.get_base_cmd()
            cmd = base_cmd + ['-U', username, 'test']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            details = {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            if result.returncode == 0:
                return True, "Face recognized successfully", details
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                return False, f"Face not recognized: {error_msg}", details
        except subprocess.TimeoutExpired:
            return False, "Timeout: Recognition test took too long", {}
        except Exception as e:
            return False, f"Error testing recognition: {str(e)}", {}
    
    def format_model_info(self, model: Dict) -> str:
        """Format model information for display"""
        label = model.get('label', 'Unknown')
        model_id = model.get('id', '?')
        timestamp = model.get('time', 0)
        
        if timestamp:
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = 'Unknown date'
        
        return f"ID: {model_id} | {label} | Added: {date_str}"
