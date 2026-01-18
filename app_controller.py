import psutil
import subprocess
import time
from typing import List, Dict, Any

# Close all running user applications safely
# Use psutil to terminate processes
# Restore applications using executable paths
# Handle errors if app is missing

class AppController:
    def __init__(self):
        self.system_processes = {
            "svchost", "csrss", "lsass", "services", "wininit",
            "dwm", "system", "explorer", "searchindexer", "wmiprvse",
            "nvidia", "amd", "intel", "nvidia-smi", "python"
        }
    
    def close_all_apps(self) -> Dict[str, Any]:
        """Close all running user applications safely"""
        closed_apps = []
        failed_apps = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    name = proc.info['name'].lower()
                    
                    # Skip system processes
                    if any(sys_proc in name for sys_proc in self.system_processes):
                        continue
                    
                    # Skip explorer (Windows Explorer)
                    if 'explorer' in name:
                        continue
                    
                    # Try to terminate the process
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    
                    # Wait for termination, force kill if needed
                    try:
                        process.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        process.kill()
                    
                    closed_apps.append(proc.info['name'])
                    print(f"Closed: {proc.info['name']}")
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, PermissionError):
                    failed_apps.append(proc.info['name'])
                    continue
                    
        except Exception as e:
            print(f"Error closing apps: {e}")
        
        return {
            'closed': closed_apps,
            'failed': failed_apps,
            'total': len(closed_apps)
        }
    
    def restore_workspace(self, apps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Restore applications using executable paths"""
        restored_apps = []
        failed_apps = []
        
        # Give the system time to settle after closing apps
        time.sleep(1)
        
        for app in apps:
            try:
                exe_path = app.get('exe')
                if exe_path and os.path.exists(exe_path):
                    subprocess.Popen([exe_path])
                    restored_apps.append(app['name'])
                    print(f"Restored: {app['name']}")
                    time.sleep(0.5)  # Small delay between app launches
                else:
                    failed_apps.append(f"{app['name']} (path not found)")
                    print(f"Could not find: {exe_path}")
            except Exception as e:
                failed_apps.append(f"{app['name']} ({str(e)})")
                print(f"Error restoring {app['name']}: {e}")
        
        return {
            'restored': restored_apps,
            'failed': failed_apps,
            'total': len(restored_apps)
        }


# Import os for path checking
import os
