import json
import os
from datetime import datetime
from typing import List, Dict, Any
import psutil

# Detect currently running user applications
# Ignore system processes
# Save process name, executable path, and window title
# Store data in JSON file inside sessions folder
# Load session data when restoring

class SessionManager:
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = sessions_dir
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)
    
    def get_running_apps(self) -> List[Dict[str, Any]]:
        """Detect currently running user applications"""
        apps = []
        system_processes = {
            "svchost", "csrss", "lsass", "services", "wininit",
            "dwm", "system", "explorer", "searchindexer", "wmiprvse",
            "nvidia", "amd", "intel", "nvidia-smi"
        }
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    name = proc.info['name'].lower()
                    exe = proc.info['exe']
                    
                    # Skip system processes
                    if any(sys_proc in name for sys_proc in system_processes):
                        continue
                    
                    # Skip if no executable path
                    if not exe:
                        continue
                    
                    apps.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': exe
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error getting running apps: {e}")
        
        return apps
    
    def save_session(self, session_name: str = None) -> str:
        """Save current workspace session to JSON file"""
        if not session_name:
            session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        apps = self.get_running_apps()
        session_data = {
            'name': session_name,
            'timestamp': datetime.now().isoformat(),
            'apps': apps
        }
        
        filepath = os.path.join(self.sessions_dir, f"{session_name}.json")
        
        try:
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"Session saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving session: {e}")
            return None
    
    def load_session(self, session_name: str) -> List[Dict[str, Any]]:
        """Load session data from JSON file"""
        filepath = os.path.join(self.sessions_dir, f"{session_name}.json")
        
        try:
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            return session_data.get('apps', [])
        except Exception as e:
            print(f"Error loading session: {e}")
            return []
    
    def list_sessions(self) -> List[str]:
        """List all saved sessions"""
        try:
            sessions = [f[:-5] for f in os.listdir(self.sessions_dir) if f.endswith('.json')]
            return sorted(sessions, reverse=True)
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []
