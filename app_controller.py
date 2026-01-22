import psutil
import subprocess
import time
import os
from typing import List, Dict, Any


class AppController:
    def __init__(self):
        # Critical system & dev tools to NEVER close
        self.system_processes = {
            "svchost", "csrss", "lsass", "services", "wininit",
            "dwm", "system", "explorer", "searchindexer", "wmiprvse",
            "nvidia", "amd", "intel", "nvidia-smi",

            # 🔒 DEV / SHELL SAFETY
            "code",            # VS Code
            "cmd",             # Command Prompt
            "powershell",      # PowerShell
            "windowsterminal", # Windows Terminal
            "python"           # Current running script
            "conhost",
            "terminal",
            "wt",          # Windows Terminal

        }
        
        # Store current process PID (self-protection)
        self.current_pid = os.getpid()

    def close_all_apps(self) -> Dict[str, Any]:
        """Close all running user applications safely"""
        closed_apps = []
        failed_apps = []

        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    pid = proc.info['pid']
                    name = (proc.info['name'] or "").lower()

                    # 🛑 Never kill yourself
                    if pid == self.current_pid:
                        continue

                    # 🛑 Skip protected processes
                    if any(sys_proc in name for sys_proc in self.system_processes):
                        continue

                    process = psutil.Process(pid)
                    process.terminate()

                    try:
                        process.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        process.kill()

                    closed_apps.append(proc.info['name'])
                    print(f"Closed: {proc.info['name']}")

                except (psutil.NoSuchProcess, psutil.AccessDenied, PermissionError):
                    failed_apps.append(proc.info.get('name', 'Unknown'))
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

        time.sleep(1)

        for app in apps:
            try:
                exe_path = app.get('exe')
                if exe_path and os.path.exists(exe_path):
                    subprocess.Popen([exe_path])
                    restored_apps.append(app['name'])
                    print(f"Restored: {app['name']}")
                    time.sleep(0.5)
                else:
                    failed_apps.append(f"{app['name']} (path not found)")
            except Exception as e:
                failed_apps.append(f"{app['name']} ({str(e)})")

        return {
            'restored': restored_apps,
            'failed': failed_apps,
            'total': len(restored_apps)
        }
