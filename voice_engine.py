import speech_recognition as sr
import pyttsx3
from typing import Optional

# Use SpeechRecognition library to listen to microphone input
# Convert speech to text using Google Speech API
# Recognize commands:
# "save workspace", "close all apps", "restore workspace"
# Handle background noise and timeouts
# Return recognized command as lowercase text

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
    def listen_for_command(self) -> Optional[str]:
        """Listen to microphone and convert speech to text"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                
            # Try to recognize speech using Google Speech Recognition API
            command = self.recognizer.recognize_google(audio)
            return command.lower().strip()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("No speech detected (timeout)")
            return None
    
    def recognize_command(self, text: str) -> Optional[str]:
        """Extract recognized command from text"""
        if not text:
            return None
            
        keywords = {
            "save": ["save", "saved"],
            "close": ["close", "closing"],
            "restore": ["restore", "restoring"],
            "start": ["start", "begin"],
            "stop": ["stop", "halt", "quit", "exit"]
        }
        
        for command, keywords_list in keywords.items():
            for keyword in keywords_list:
                if keyword in text:
                    return command
        
        return None
    
    def speak(self, message: str):
        """Use text-to-speech to provide audio feedback"""
        try:
            self.engine.say(message)
            # Use a non-blocking approach
            self.engine.setProperty('_inLoop', False)
            self.engine.iterate()
        except RuntimeError:
            # If event loop is already running, skip TTS
            pass
        except Exception as e:
            print(f"TTS error: {e}")
