import threading
import time
from voice_engine import VoiceEngine
from hotkeys import HotKeyListener
from session_manager import SessionManager
from app_controller import AppController

# Entry point of the application
# Start voice listener in a separate thread
# Start hotkey listener
# Map commands to functions:
# save_workspace
# close_all_apps
# restore_workspace
# Keep program running

class Rose:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.hotkey_listener = HotKeyListener()
        self.session_manager = SessionManager()
        self.app_controller = AppController()
        self.current_session = None
        self.is_running = False
        self.voice_thread_active = False
    
    def save_workspace(self):
        """Save current workspace"""
        print("\n💾 Saving workspace...")
        self.voice_engine.speak("Saving workspace")
        
        filepath = self.session_manager.save_session()
        if filepath:
            self.current_session = filepath
            self.voice_engine.speak("Workspace saved successfully")
            print("✅ Workspace saved successfully!")
        else:
            self.voice_engine.speak("Failed to save workspace")
            print("❌ Failed to save workspace")
    
    def close_all_apps(self):
        """Close all running applications"""
        print("\n🛑 Closing all applications...")
        self.voice_engine.speak("Closing all applications")
        
        result = self.app_controller.close_all_apps()
        print(f"✅ Closed {result['total']} application(s)")
        self.voice_engine.speak(f"Closed {result['total']} applications")
    
    def restore_workspace(self):
        """Restore saved workspace"""
        print("\n♻️ Restoring workspace...")
        self.voice_engine.speak("Restoring workspace")
        
        # Get the most recent session
        sessions = self.session_manager.list_sessions()
        if sessions:
            apps = self.session_manager.load_session(sessions[0])
            result = self.app_controller.restore_workspace(apps)
            print(f"✅ Restored {result['total']} application(s)")
            self.voice_engine.speak(f"Restored {result['total']} applications")
        else:
            self.voice_engine.speak("No saved sessions found")
            print("❌ No saved sessions found")
    
    def voice_listener_thread(self):
        """Listen for voice commands in a separate thread"""
        print("🎤 Voice listener started")
        
        while self.is_running:
            try:
                command_text = self.voice_engine.listen_for_command()
                
                if command_text:
                    print(f"Heard: {command_text}")
                    command = self.voice_engine.recognize_command(command_text)
                    
                    if command == "save":
                        self.save_workspace()
                    elif command == "close":
                        self.close_all_apps()
                    elif command == "restore":
                        self.restore_workspace()
                    elif command == "stop":
                        print("🛑 Stop command received from voice")
                        self.voice_engine.speak("Stopping Rose")
                        self.stop()
                    elif command == "start":
                        if not self.voice_thread_active:
                            print("▶️ Start command received")
                            self.voice_engine.speak("Rose is already running")
                        else:
                            print("▶️ Start command received")
                            self.voice_engine.speak("Rose started")
                    else:
                        print(f"Command not recognized: {command_text}")
                        self.voice_engine.speak("Command not recognized")
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Voice listener error: {e}")
                self.voice_engine.speak("An error occurred in voice recognition")
    
    def register_hotkey_callbacks(self):
        """Register hotkey callbacks"""
        self.hotkey_listener.register_command('save', self.save_workspace)
        self.hotkey_listener.register_command('close', self.close_all_apps)
        self.hotkey_listener.register_command('restore', self.restore_workspace)
    
    def start(self):
        """Start the Rose application"""
        print("="*50)
        print("🌹 Rose - Voice Workspace Manager")
        print("="*50)
        print("\nCommands:")
        print("  Voice: 'save workspace', 'close all apps', 'restore workspace'")
        print("  Voice Control: 'start', 'stop'")
        print("  Hotkeys: Ctrl+Alt+S (save), Ctrl+Alt+C (close), Ctrl+Alt+R (restore)")
        print("\nStarting Rose...\n")
        
        self.is_running = True
        self.voice_thread_active = True
        
        # Register hotkey callbacks
        self.register_hotkey_callbacks()
        
        # Start voice listener thread
        voice_thread = threading.Thread(target=self.voice_listener_thread, daemon=True)
        voice_thread.start()
        
        # Start hotkey listener thread
        hotkey_thread = self.hotkey_listener.start_in_thread()
        
        # Keep the program running
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down Rose...")
            self.stop()
    
    def stop(self):
        """Stop the application"""
        self.is_running = False
        self.voice_thread_active = False
        self.hotkey_listener.stop_listening()
        print("✅ Rose stopped")


if __name__ == "__main__":
    app = Rose()
    app.start()
