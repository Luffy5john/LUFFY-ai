"""
L.U.F.F.Y - Working Voice Version
Fixed voice input issues for Python 3.13
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

# Check for speech recognition
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_AVAILABLE = True
    print("Voice recognition available")
except ImportError as e:
    VOICE_AVAILABLE = False
    print(f"Voice not available: {e}")

# Check for text-to-speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
    print("Text-to-speech available")
except ImportError:
    TTS_AVAILABLE = False
    print("TTS not available")

class LUFFYWorking:
    def __init__(self):
        self.conversation_history = []
        self.setup_voice()
        
        # Personality responses
        self.greetings = [
            "Good morning, captain. How may I assist you today?",
            "At your service, captain.",
            "How can I help you today?",
            "Ready for your commands, captain."
        ]
    
    def setup_voice(self):
        """Setup voice recognition and TTS"""
        if VOICE_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Test microphone
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone ready")
            except Exception as e:
                print(f"Microphone setup failed: {e}")
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 0.9)
                print("TTS ready")
            except Exception as e:
                print(f"TTS setup failed: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"L.U.F.F.Y: {text}")
        if TTS_AVAILABLE:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
    
    def listen_once(self):
        """Listen for a single voice command"""
        if not VOICE_AVAILABLE:
            return None
        
        try:
            print("Listening for voice input...")
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
            
            print("Processing speech...")
            # Recognize speech using Google
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"Recognized: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            return None
    
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

class LUFFYWorkingGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("L.U.F.F.Y - Working Voice AI")
        self.root.geometry("800x650")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize L.U.F.F.Y
        self.luffy = LUFFYWorking()
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
        voice_status = "VOICE READY" if VOICE_AVAILABLE else "TEXT ONLY"
        tts_status = "TTS ON" if TTS_AVAILABLE else "TTS OFF"
        self.status_label = ttk.Label(self.root, text=f"● ONLINE - {voice_status} - {tts_status}", style='Status.TLabel')
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
            height=15
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
        self.command_entry.pack(fill=tk.X, pady=(0, 10))
        self.command_entry.bind('<Return>', self.send_command)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#0a0a0a')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.send_button = ttk.Button(
            button_frame, 
            text="Send", 
            command=self.send_command,
            style='LUFFY.TButton'
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Voice button (only if speech is available)
        if VOICE_AVAILABLE:
            self.listen_button = ttk.Button(
                button_frame, 
                text="🎤 Voice Command", 
                command=self.voice_command,
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
        if VOICE_AVAILABLE:
            welcome_msg += " Click 'Voice Command' to speak."
        else:
            welcome_msg += " Voice unavailable - text input only."
        
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
            if TTS_AVAILABLE:
                threading.Thread(target=lambda: self.luffy.speak(response), daemon=True).start()
            
            # Check for exit
            if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                self.root.after(2000, self.root.quit)
    
    def voice_command(self):
        """Handle single voice command"""
        if not VOICE_AVAILABLE:
            self.add_to_chat("L.U.F.F.Y", "Voice recognition not available, captain.")
            return
        
        # Update button and status
        self.listen_button.config(text="🎤 Listening...", state='disabled')
        self.status_label.config(text="● LISTENING", foreground='#ffff00')
        
        def listen_worker():
            try:
                # Listen for command
                command = self.luffy.listen_once()
                
                if command:
                    # Update GUI in main thread
                    self.root.after(0, lambda: self.add_to_chat("You", command))
                    
                    # Process command
                    response = self.luffy.process_command(command)
                    self.root.after(0, lambda: self.add_to_chat("L.U.F.F.Y", response))
                    
                    # Speak response
                    if TTS_AVAILABLE:
                        self.luffy.speak(response)
                    
                    # Check for exit
                    if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'bye']):
                        self.root.after(2000, self.root.quit)
                else:
                    self.root.after(0, lambda: self.add_to_chat("L.U.F.F.Y", "I didn't hear anything, captain. Try again."))
                
            except Exception as e:
                self.root.after(0, lambda: self.add_to_chat("L.U.F.F.Y", f"Voice error: {str(e)}"))
            
            finally:
                # Reset button and status
                voice_status = "VOICE READY" if VOICE_AVAILABLE else "TEXT ONLY"
                tts_status = "TTS ON" if TTS_AVAILABLE else "TTS OFF"
                self.root.after(0, lambda: self.listen_button.config(text="🎤 Voice Command", state='normal'))
                self.root.after(0, lambda: self.status_label.config(text=f"● ONLINE - {voice_status} - {tts_status}", foreground='#00ff00'))
        
        # Start listening in separate thread
        threading.Thread(target=listen_worker, daemon=True).start()
    
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
    app = LUFFYWorkingGui()
    app.run()
