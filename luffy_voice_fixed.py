"""
L.U.F.F.Y - Voice-Enabled Version with Python 3.13 Compatibility
Uses Windows Speech API as fallback
"""

import datetime
import webbrowser
import os
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import re
import math
import random

# Try multiple speech recognition options
SPEECH_METHOD = None

# Option 1: Try SpeechRecognition library
try:
    import speech_recognition as sr
    SPEECH_METHOD = "sr"
    print("Using SpeechRecognition library")
except ImportError:
    pass

# Option 2: Try Windows Speech API
if SPEECH_METHOD is None:
    try:
        import win32com.client
        SPEECH_METHOD = "win32"
        print("Using Windows Speech API")
    except ImportError:
        pass

# Text-to-Speech options
TTS_METHOD = None

# Option 1: Try pyttsx3
try:
    import pyttsx3
    TTS_METHOD = "pyttsx3"
    print("Using pyttsx3 for TTS")
except ImportError:
    pass

# Option 2: Try Windows SAPI
if TTS_METHOD is None:
    try:
        import win32com.client
        TTS_METHOD = "sapi"
        print("Using Windows SAPI for TTS")
    except ImportError:
        print("No TTS available - text output only")

class LUFFYVoice:
    def __init__(self):
        self.conversation_history = []
        self.setup_speech()
        self.setup_tts()
        
        # Personality responses
        self.greetings = [
            "Good morning, captain. How may I assist you today?",
            "At your service, captain.",
            "How can I help you today?",
            "Ready for your commands, captain."
        ]
        
        self.confirmations = [
            "Right away, captain.",
            "Consider it done.",
            "Certainly, captain.",
            "Of course."
        ]
    
    def setup_speech(self):
        """Setup speech recognition"""
        if SPEECH_METHOD == "sr":
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                print("Speech recognition ready")
            except:
                print("Speech recognition setup failed")
        elif SPEECH_METHOD == "win32":
            try:
                self.speech_context = win32com.client.Dispatch("SAPI.SpInProcRecoContext")
                print("Windows speech recognition ready")
            except:
                print("Windows speech recognition setup failed")
    
    def setup_tts(self):
        """Setup text-to-speech"""
        if TTS_METHOD == "pyttsx3":
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                # Try to find a male voice
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 0.9)
                print("TTS ready")
            except:
                print("TTS setup failed")
        elif TTS_METHOD == "sapi":
            try:
                self.sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
                print("Windows TTS ready")
            except:
                print("Windows TTS setup failed")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"L.U.F.F.Y: {text}")
        
        if TTS_METHOD == "pyttsx3":
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
        elif TTS_METHOD == "sapi":
            try:
                self.sapi_voice.Speak(text)
            except:
                pass
    
    def listen(self):
        """Listen for voice commands"""
        if SPEECH_METHOD == "sr":
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except:
                return None
        else:
            return None  # No speech recognition available
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        return now.strftime("The current time is %I:%M %p, captain.")
    
    def get_current_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        return now.strftime("Today is %A, %B %d, %Y.")
    
    def calculate(self, expression):
        """Perform mathematical calculations"""
        try:
            expression = expression.replace('x', '*').replace('÷', '/')
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"The answer is {result}, captain."
            else:
                return "I can only perform basic mathematical operations, captain."
        except:
            return "I couldn't calculate that, captain. Please check your expression."
    
    def search_web(self, query):
        """Search the web"""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"I've opened a web search for '{query}' in your browser, captain."
    
    def open_application(self, app_name):
        """Open applications"""
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'browser': 'start chrome',
            'chrome': 'start chrome',
            'firefox': 'start firefox',
            'edge': 'start msedge',
            'file explorer': 'explorer.exe',
            'explorer': 'explorer.exe'
        }
        
        app_name = app_name.lower()
        if app_name in apps:
            try:
                if 'start' in apps[app_name]:
                    os.system(apps[app_name])
                else:
                    subprocess.Popen(apps[app_name])
                return f"Opening {app_name}, captain."
            except:
                return f"I couldn't open {app_name}, captain."
        else:
            return f"I don't know how to open {app_name}, captain."
    
    def process_command(self, command):
        """Process and execute commands"""
        if not command:
            return "Please enter a command, captain."
        
        original_command = command
        command = command.lower()
        
        # Store conversation
        self.conversation_history.append({"user": original_command, "timestamp": datetime.datetime.now()})
        
        # Greetings
        if any(word in command for word in ['hello', 'hi', 'hey', 'luffy']):
            response = random.choice(self.greetings)
            return response
        
        # Time queries
        elif 'time' in command:
            return self.get_current_time()
        
        # Date queries
        elif 'date' in command or 'today' in command:
            return self.get_current_date()
        
        # Calculations
        elif any(word in command for word in ['calculate', 'compute', 'math', '+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            math_pattern = r'[\d+\-*/().]+|plus|minus|times|divided by'
            expression = ' '.join(re.findall(math_pattern, command))
            expression = expression.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
            if expression:
                return self.calculate(expression)
            else:
                return "Please provide a mathematical expression, captain."
        
        # Web search
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            if query:
                return self.search_web(query)
            else:
                return "What would you like me to search for, captain?"
        
        # Open applications
        elif 'open' in command:
            app = command.replace('open', '').strip()
            return self.open_application(app)
        
        # Exit commands
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            return "Goodbye, captain. It was a pleasure serving you."
        
        # Unknown command
        else:
            responses = [
                "I'm not sure I understand that command, captain.",
                "Could you please rephrase that, captain?",
                "I didn't quite catch that, captain."
            ]
            return random.choice(responses)

class LUFFYVoiceGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("L.U.F.F.Y - Voice AI Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize L.U.F.F.Y
        self.luffy = LUFFYVoice()
        self.listening = False
        
        self.setup_gui()
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       background='#0a0a0a', 
                       foreground='#00ffff', 
                       font=('Arial', 24, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#0a0a0a', 
                       foreground='#00ff00', 
                       font=('Arial', 12))
        
        style.configure('LUFFY.TButton',
                       background='#1a1a1a',
                       foreground='#00ffff',
                       font=('Arial', 12, 'bold'),
                       borderwidth=2)
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Title
        title_label = ttk.Label(self.root, text="L.U.F.F.Y", style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.root, 
                                  text="Learning Universal Friendly Framework for You", 
                                  background='#0a0a0a', 
                                  foreground='#888888', 
                                  font=('Arial', 12, 'italic'))
        subtitle_label.pack(pady=(0, 20))
        
        # Status indicator
        voice_status = "VOICE READY" if SPEECH_METHOD else "TEXT ONLY"
        self.status_label = ttk.Label(self.root, text=f"● ONLINE - {voice_status}", style='Status.TLabel')
        self.status_label.pack(pady=10)
        
        # Chat display
        chat_frame = tk.Frame(self.root, bg='#0a0a0a')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#0a0a0a')
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.command_entry = tk.Entry(
            input_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Arial', 12),
            insertbackground='#00ffff'
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.command_entry.bind('<Return>', self.send_command)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#0a0a0a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.send_button = ttk.Button(
            button_frame, 
            text="Send", 
            command=self.send_command,
            style='LUFFY.TButton'
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Voice button (only if speech is available)
        if SPEECH_METHOD:
            self.listen_button = ttk.Button(
                button_frame, 
                text="🎤 Listen", 
                command=self.toggle_listening,
                style='LUFFY.TButton'
            )
            self.listen_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_chat,
            style='LUFFY.TButton'
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Initialize
        welcome_msg = "System initialized. Ready for commands, captain."
        if SPEECH_METHOD:
            welcome_msg += " Voice recognition is active."
        else:
            welcome_msg += " Voice recognition unavailable - using text input."
        
        self.add_to_chat("L.U.F.F.Y", welcome_msg)
        
    def add_to_chat(self, sender, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        
        if sender == "L.U.F.F.Y":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"L.U.F.F.Y: ", 'luffy')
            self.chat_display.insert(tk.END, f"{message}\n", 'luffy_text')
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"You: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n", 'user_text')
        
        # Configure text tags
        self.chat_display.tag_config('timestamp', foreground='#888888')
        self.chat_display.tag_config('luffy', foreground='#00ffff', font=('Arial', 11, 'bold'))
        self.chat_display.tag_config('luffy_text', foreground='#ffffff')
        self.chat_display.tag_config('user', foreground='#00ff00', font=('Arial', 11, 'bold'))
        self.chat_display.tag_config('user_text', foreground='#ffffff')
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_command(self, event=None):
        """Send text command"""
        command = self.command_entry.get().strip()
        if command:
            self.add_to_chat("You", command)
            self.command_entry.delete(0, tk.END)
            
            # Process command
            response = self.luffy.process_command(command)
            self.add_to_chat("L.U.F.F.Y", response)
            
            # Speak response if TTS available
            if TTS_METHOD:
                threading.Thread(target=lambda: self.luffy.speak(response), daemon=True).start()
            
            # Check for exit
            if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                self.root.after(2000, self.root.quit)
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not SPEECH_METHOD:
            return
        
        if not self.listening:
            self.listening = True
            self.listen_button.config(text="🛑 Stop")
            self.status_label.config(text="● LISTENING", foreground='#ffff00')
            threading.Thread(target=self.listen_thread, daemon=True).start()
        else:
            self.listening = False
            self.listen_button.config(text="🎤 Listen")
            self.status_label.config(text="● ONLINE - VOICE READY", foreground='#00ff00')
    
    def listen_thread(self):
        """Voice listening thread"""
        while self.listening:
            try:
                command = self.luffy.listen()
                if command and self.listening:
                    self.root.after(0, lambda cmd=command: self.add_to_chat("You", cmd))
                    response = self.luffy.process_command(command)
                    self.root.after(0, lambda resp=response: self.add_to_chat("L.U.F.F.Y", resp))
                    
                    # Speak response
                    if TTS_METHOD:
                        threading.Thread(target=lambda: self.luffy.speak(response), daemon=True).start()
                    
                    # Check for exit
                    if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                        self.root.after(2000, self.root.quit)
                        break
            except Exception as e:
                print(f"Listening error: {e}")
                break
        
        self.listening = False
        if hasattr(self, 'listen_button'):
            self.root.after(0, lambda: self.listen_button.config(text="🎤 Listen"))
        self.root.after(0, lambda: self.status_label.config(text="● ONLINE - VOICE READY", foreground='#00ff00'))
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_to_chat("L.U.F.F.Y", "Chat cleared. How may I assist you, captain?")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LUFFYVoiceGui()
    app.run()
