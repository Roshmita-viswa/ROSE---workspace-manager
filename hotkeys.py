import keyboard
import threading
from typing import Callable, Dict

# Register global keyboard shortcuts using keyboard library
# Ctrl+Alt+S -> save workspace
# Ctrl+Alt+C -> close all apps
# Ctrl+Alt+R -> restore workspace
# Keep listener running in background

class HotKeyListener:
    def __init__(self):
        self.is_running = False
        self.listeners = {}
        self.command_callbacks: Dict[str, Callable] = {}
    
    def register_command(self, command: str, callback: Callable):
        """Register a callback for a command"""
        self.command_callbacks[command] = callback
    
    def on_save_workspace(self):
        """Handle save workspace hotkey"""
        if 'save' in self.command_callbacks:
            self.command_callbacks['save']()
    
    def on_close_apps(self):
        """Handle close all apps hotkey"""
        if 'close' in self.command_callbacks:
            self.command_callbacks['close']()
    
    def on_restore_workspace(self):
        """Handle restore workspace hotkey"""
        if 'restore' in self.command_callbacks:
            self.command_callbacks['restore']()
    
    def start_listening(self):
        """Start listening for keyboard shortcuts"""
        if self.is_running:
            return
        
        self.is_running = True
        print("Hotkey listener started")
        
        # Register hotkeys
        keyboard.add_hotkey('ctrl+alt+s', self.on_save_workspace)
        keyboard.add_hotkey('ctrl+alt+c', self.on_close_apps)
        keyboard.add_hotkey('ctrl+alt+r', self.on_restore_workspace)
        
        # Keep the listener active
        try:
            keyboard.wait()
        except Exception as e:
            print(f"Hotkey listener error: {e}")
    
    def stop_listening(self):
        """Stop listening for keyboard shortcuts"""
        self.is_running = False
        keyboard.unhook_all()
        print("Hotkey listener stopped")
    
    def start_in_thread(self):
        """Start hotkey listener in a separate thread"""
        listener_thread = threading.Thread(target=self.start_listening, daemon=True)
        listener_thread.start()
        return listener_thread
