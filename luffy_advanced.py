import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import datetime
import os
import subprocess
import webbrowser
import json
import requests
import psutil
import platform
import socket
import winreg
from pathlib import Path

# Voice and TTS imports with fallbacks
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Voice recognition not available - install speechrecognition and pyaudio")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Text-to-speech not available - install pyttsx3")

class AdvancedLUFFY:
    def __init__(self):
        self.setup_voice()
        self.setup_data_storage()
        self.load_user_preferences()
        self.wake_word_active = False
        self.listening_thread = None
        
    def setup_voice(self):
        """Initialize voice recognition and TTS"""
        if VOICE_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🎤 Voice recognition ready")
            except Exception as e:
                print(f"Voice setup failed: {e}")
                
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 180)
                self.tts_engine.setProperty('volume', 0.9)
                print("🔊 Text-to-speech ready")
            except Exception as e:
                print(f"TTS setup failed: {e}")
    
    def setup_data_storage(self):
        """Create data directories and files"""
        self.data_dir = Path("luffy_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize data files
        self.preferences_file = self.data_dir / "preferences.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.contacts_file = self.data_dir / "contacts.json"
        self.automation_file = self.data_dir / "automation.json"
        
    def load_user_preferences(self):
        """Load user preferences and settings"""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r') as f:
                    self.preferences = json.load(f)
            else:
                self.preferences = {
                    "name": "Captain",
                    "voice_enabled": True,
                    "auto_weather": True,
                    "news_sources": ["bbc", "cnn"],
                    "work_hours": {"start": "09:00", "end": "17:00"}
                }
                self.save_preferences()
        except Exception as e:
            print(f"Error loading preferences: {e}")
            self.preferences = {}
    
    def save_preferences(self):
        """Save user preferences"""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"L.U.F.F.Y: {text}")
        if TTS_AVAILABLE and self.preferences.get("voice_enabled", True):
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
    
    def listen(self):
        """Listen for voice commands"""
        if not VOICE_AVAILABLE:
            return None
            
        try:
            print("Adjusting for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("Listening for command...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing speech...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")
            return None
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return None
    
    def start_wake_word_listening(self):
        """Start continuous listening for wake word 'Hey L.U.F.F.Y'"""
        if not VOICE_AVAILABLE:
            return
            
        self.wake_word_active = True
        
        def wake_word_loop():
            print("🎤 Wake word detection started - say 'Hey L.U.F.F.Y'")
            
            while self.wake_word_active:
                try:
                    with self.microphone as source:
                        # Listen for wake word with shorter timeout
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    # Process audio for wake word
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                        
                        # Check for wake words
                        wake_words = ["hey luffy", "hey l.u.f.f.y", "luffy", "hey jarvis"]
                        
                        if any(wake_word in text for wake_word in wake_words):
                            print(f"🎤 Wake word detected: {text}")
                            self.speak("Yes captain, I'm listening.")
                            
                            # Listen for the actual command
                            command = self.listen_for_command()
                            if command:
                                # Notify GUI about wake word activation
                                if hasattr(self, 'gui_callback'):
                                    self.gui_callback("wake_word", text, command)
                                    
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        continue
                        
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    if self.wake_word_active:  # Only print if still active
                        print(f"Wake word detection error: {e}")
                    continue
        
        self.listening_thread = threading.Thread(target=wake_word_loop, daemon=True)
        self.listening_thread.start()
    
    def stop_wake_word_listening(self):
        """Stop continuous listening"""
        self.wake_word_active = False
        print("🎤 Wake word detection stopped")
    
    def listen_for_command(self):
        """Listen for command after wake word is detected"""
        try:
            print("🎤 Listening for your command...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"🎤 Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything, captain.")
            return None
        except sr.UnknownValueError:
            self.speak("I didn't understand that, captain.")
            return None
        except Exception as e:
            print(f"Command listening error: {e}")
            return None
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "memory_available": f"{memory.available // (1024**3)} GB",
                "disk_usage": f"{disk.percent}%",
                "disk_free": f"{disk.free // (1024**3)} GB",
                "platform": platform.system(),
                "processor": platform.processor(),
                "hostname": socket.gethostname()
            }
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def control_system(self, command):
        """System control commands"""
        command = command.lower()
        
        if "shutdown" in command:
            self.speak("Shutting down system in 30 seconds. Say 'cancel shutdown' to abort.")
            subprocess.run(["shutdown", "/s", "/t", "30"])
            return "System shutdown initiated"
            
        elif "restart" in command or "reboot" in command:
            self.speak("Restarting system in 30 seconds.")
            subprocess.run(["shutdown", "/r", "/t", "30"])
            return "System restart initiated"
            
        elif "cancel shutdown" in command:
            subprocess.run(["shutdown", "/a"])
            return "Shutdown cancelled"
            
        elif "lock" in command:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return "System locked"
            
        elif "sleep" in command:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
            return "System entering sleep mode"
            
        elif "volume up" in command:
            subprocess.run(["nircmd.exe", "changesysvolume", "5000"])
            return "Volume increased"
            
        elif "volume down" in command:
            subprocess.run(["nircmd.exe", "changesysvolume", "-5000"])
            return "Volume decreased"
            
        elif "mute" in command:
            subprocess.run(["nircmd.exe", "mutesysvolume", "1"])
            return "System muted"
            
        elif "unmute" in command:
            subprocess.run(["nircmd.exe", "mutesysvolume", "0"])
            return "System unmuted"
            
        return "System command not recognized"
    
    def find_installed_apps(self):
        """Discover installed applications on the system"""
        apps = {}
        
        # Common system applications
        system_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "outlook": "outlook.exe"
        }
        apps.update(system_apps)
        
        # Search common installation directories
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.path.expanduser("~\\AppData\\Local"),
            os.path.expanduser("~\\AppData\\Roaming")
        ]
        
        common_apps = [
            "chrome.exe", "firefox.exe", "msedge.exe", "opera.exe",
            "code.exe", "notepad++.exe", "sublime_text.exe", "atom.exe",
            "discord.exe", "slack.exe", "teams.exe", "zoom.exe",
            "spotify.exe", "vlc.exe", "winamp.exe", "itunes.exe",
            "steam.exe", "epicgameslauncher.exe", "origin.exe",
            "photoshop.exe", "illustrator.exe", "premiere.exe",
            "obs64.exe", "obs32.exe", "streamlabs obs.exe",
            "blender.exe", "unity.exe", "unrealengine.exe",
            "python.exe", "java.exe", "javaw.exe"
        ]
        
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path):
                        # Limit depth to avoid too much scanning
                        depth = root[len(search_path):].count(os.sep)
                        if depth > 3:
                            continue
                            
                        for file in files:
                            if file.lower().endswith('.exe'):
                                file_lower = file.lower()
                                app_name = file_lower.replace('.exe', '').replace('_', ' ').replace('-', ' ')
                                full_path = os.path.join(root, file)
                                
                                # Add common applications
                                if file_lower in [app.lower() for app in common_apps]:
                                    apps[app_name] = full_path
                                    
                                # Add applications with common names
                                if any(keyword in app_name for keyword in ['chrome', 'firefox', 'code', 'discord', 'spotify', 'steam', 'obs', 'photoshop', 'blender']):
                                    apps[app_name] = full_path
                                    
                except (PermissionError, OSError):
                    continue
        
        return apps
    
    def open_application(self, app_name):
        """Open applications by name with dynamic discovery"""
        app_name = app_name.lower().strip()
        
        # Get all available apps
        available_apps = self.find_installed_apps()
        
        # Direct match
        if app_name in available_apps:
            try:
                app_path = available_apps[app_name]
                if app_name == "settings":
                    subprocess.run(["start", app_path], shell=True)
                else:
                    subprocess.run([app_path], shell=True)
                return f"Opening {app_name.title()}"
            except Exception as e:
                return f"Could not open {app_name}: {str(e)}"
        
        # Partial match search
        matches = []
        for app, path in available_apps.items():
            if app_name in app or any(word in app for word in app_name.split()):
                matches.append((app, path))
        
        if matches:
            # Use the best match (shortest name usually most relevant)
            best_match = min(matches, key=lambda x: len(x[0]))
            app, path = best_match
            try:
                if "settings" in app:
                    subprocess.run(["start", path], shell=True)
                else:
                    subprocess.run([path], shell=True)
                return f"Opening {app.title()} (matched from '{app_name}')"
            except Exception as e:
                return f"Could not open {app}: {str(e)}"
        
        # Try Windows Start command as fallback
        try:
            subprocess.run(["start", "", app_name], shell=True)
            return f"Attempting to open {app_name} via Windows Start"
        except Exception as e:
            # Final fallback - try to find in PATH
            try:
                subprocess.run([app_name], shell=True)
                return f"Opening {app_name}"
            except:
                return f"Could not find application '{app_name}'. Try being more specific or check if it's installed."
    
    def get_weather(self, city=""):
        """Get weather information"""
        try:
            # Using OpenWeatherMap API (requires API key)
            api_key = "your_openweather_api_key"  # User needs to add their API key
            if not city:
                city = "London"  # Default city
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": data["name"],
                    "temperature": f"{data['main']['temp']}°C",
                    "description": data["weather"][0]["description"],
                    "humidity": f"{data['main']['humidity']}%",
                    "wind_speed": f"{data['wind']['speed']} m/s"
                }
                return f"Weather in {weather['city']}: {weather['temperature']}, {weather['description']}"
            else:
                return "Weather service unavailable"
        except Exception as e:
            return f"Could not get weather: {str(e)}"
    
    def search_web(self, query):
        """Search the web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for: {query}"
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def file_operations(self, command, path=""):
        """File and folder operations"""
        command = command.lower()
        
        if "create folder" in command:
            folder_name = command.replace("create folder", "").strip()
            try:
                os.makedirs(folder_name, exist_ok=True)
                return f"Created folder: {folder_name}"
            except Exception as e:
                return f"Could not create folder: {str(e)}"
                
        elif "delete file" in command:
            file_name = command.replace("delete file", "").strip()
            try:
                os.remove(file_name)
                return f"Deleted file: {file_name}"
            except Exception as e:
                return f"Could not delete file: {str(e)}"
                
        elif "list files" in command:
            try:
                files = os.listdir(".")
                return f"Files in current directory: {', '.join(files[:10])}"
            except Exception as e:
                return f"Could not list files: {str(e)}"
                
        return "File operation not recognized"
    
    def calculate(self, expression):
        """Safe calculator"""
        try:
            # Remove dangerous functions
            allowed_chars = "0123456789+-*/.() "
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"{expression} = {result}"
            else:
                return "Invalid calculation"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def set_reminder(self, reminder_text, minutes=5):
        """Set a reminder"""
        def reminder_alert():
            time.sleep(minutes * 60)
            self.speak(f"Reminder: {reminder_text}")
            messagebox.showinfo("L.U.F.F.Y Reminder", reminder_text)
        
        threading.Thread(target=reminder_alert, daemon=True).start()
        return f"Reminder set for {minutes} minutes: {reminder_text}"
    
    def process_command(self, command):
        """Process and respond to commands"""
        if not command:
            return "I didn't catch that, captain."
            
        command = command.lower().strip()
        
        # Greetings
        if any(word in command for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            current_hour = datetime.datetime.now().hour
            if current_hour < 12:
                greeting = "Good morning"
            elif current_hour < 18:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"
            return f"{greeting}, {self.preferences.get('name', 'Captain')}! How can I assist you today?"
        
        # Time and date
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
            
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}"
        
        # System information
        elif "system info" in command or "system status" in command:
            info = self.get_system_info()
            return f"System Status - CPU: {info.get('cpu_usage', 'N/A')}, Memory: {info.get('memory_usage', 'N/A')}, Disk: {info.get('disk_usage', 'N/A')}"
        
        # System control
        elif any(word in command for word in ["shutdown", "restart", "lock", "sleep", "volume", "mute"]):
            return self.control_system(command)
        
        # List available applications
        elif "list apps" in command or "show apps" in command or "available apps" in command:
            apps = self.find_installed_apps()
            app_list = list(apps.keys())[:20]  # Show first 20 apps
            return f"Available applications: {', '.join(app_list)}. Say 'open [app name]' to launch any app."
        
        # Open applications
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            return self.open_application(app_name)
        
        # Weather
        elif "weather" in command:
            city = command.replace("weather", "").replace("in", "").strip()
            return self.get_weather(city)
        
        # Web search
        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            return self.search_web(query)
        
        # File operations
        elif any(word in command for word in ["create folder", "delete file", "list files"]):
            return self.file_operations(command)
        
        # Calculator
        elif "calculate" in command or "math" in command:
            expression = command.replace("calculate", "").replace("math", "").strip()
            return self.calculate(expression)
        
        # Reminders
        elif "remind me" in command:
            reminder_text = command.replace("remind me", "").strip()
            return self.set_reminder(reminder_text)
        
        # Jokes
        elif "joke" in command:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why don't programmers like nature? It has too many bugs!",
                "I'm reading a book about anti-gravity. It's impossible to put down!"
            ]
            import random
            return random.choice(jokes)
        
        # Default response
        else:
            return "I'm not sure how to help with that, captain. Try asking about time, weather, opening apps, or system information."

class LUFFYAdvancedGUI:
    def __init__(self):
        self.luffy = AdvancedLUFFY()
        self.luffy.gui_callback = self.handle_wake_word_activation
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the advanced GUI"""
        self.root = tk.Tk()
        self.root.title("L.U.F.F.Y - Advanced AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#0a0a0a')
        style.configure('Dark.TLabel', background='#0a0a0a', foreground='#00ffff')
        style.configure('Dark.TButton', background='#1a1a1a', foreground='#00ffff')
        
        self.setup_header()
        self.setup_chat_area()
        self.setup_status_bar()
        self.setup_control_panel()
        self.setup_input_area()
        
        # Start with greeting
        self.add_message("L.U.F.F.Y", "Advanced AI Assistant initialized. All systems online, captain!")
        
    def setup_header(self):
        """Setup header with title and status"""
        header_frame = tk.Frame(self.root, bg="#0a0a0a", height=60)
        header_frame.pack(fill="x", padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="L.U.F.F.Y", 
                              font=("Arial", 24, "bold"), 
                              fg="#00ffff", bg="#0a0a0a")
        title_label.pack(side="left", pady=10)
        
        subtitle_label = tk.Label(header_frame, text="Advanced AI Assistant", 
                                 font=("Arial", 12), 
                                 fg="#888888", bg="#0a0a0a")
        subtitle_label.pack(side="left", padx=(10, 0), pady=15)
        
    def setup_chat_area(self):
        """Setup main chat area"""
        chat_frame = tk.Frame(self.root, bg="#0a0a0a")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#00ffff",
            selectbackground="#333333"
        )
        self.chat_display.pack(fill="both", expand=True)
        
    def setup_status_bar(self):
        """Setup status bar"""
        status_frame = tk.Frame(self.root, bg="#0a0a0a", height=30)
        status_frame.pack(fill="x", padx=10, pady=2)
        status_frame.pack_propagate(False)
        
        voice_status = "VOICE READY" if VOICE_AVAILABLE else "TEXT ONLY"
        tts_status = "TTS ON" if TTS_AVAILABLE else "TTS OFF"
        
        self.status_label = tk.Label(status_frame, 
                                    text=f"● ONLINE - {voice_status} - {tts_status}",
                                    font=("Arial", 10), 
                                    fg="#00ff00", bg="#0a0a0a")
        self.status_label.pack(side="left")
        
        # System info on right
        info = self.luffy.get_system_info()
        sys_info = f"CPU: {info.get('cpu_usage', 'N/A')} | RAM: {info.get('memory_usage', 'N/A')}"
        self.sys_info_label = tk.Label(status_frame, text=sys_info,
                                      font=("Arial", 10), 
                                      fg="#888888", bg="#0a0a0a")
        self.sys_info_label.pack(side="right")
        
    def setup_control_panel(self):
        """Setup control panel with quick actions"""
        control_frame = tk.Frame(self.root, bg="#0a0a0a", height=50)
        control_frame.pack(fill="x", padx=10, pady=5)
        control_frame.pack_propagate(False)
        
        # Quick action buttons
        buttons = [
            ("🎤 Voice", self.voice_command),
            ("👂 Wake Word", self.toggle_wake_word),
            ("🌤️ Weather", lambda: self.quick_command("weather")),
            ("📊 System", lambda: self.quick_command("system info")),
            ("🔍 Search", self.quick_search),
            ("📁 Files", lambda: self.quick_command("list files")),
            ("🧮 Calc", self.quick_calc)
        ]
        
        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                           bg="#1a1a1a", fg="#00ffff", 
                           font=("Arial", 10), relief="flat",
                           padx=10, pady=5)
            btn.pack(side="left", padx=2)
            
    def setup_input_area(self):
        """Setup input area"""
        input_frame = tk.Frame(self.root, bg="#0a0a0a", height=40)
        input_frame.pack(fill="x", padx=10, pady=5)
        input_frame.pack_propagate(False)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                   font=("Arial", 12), bg="#1a1a1a", fg="#ffffff",
                                   insertbackground="#00ffff", relief="flat")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message,
                            bg="#00ffff", fg="#000000", font=("Arial", 10, "bold"),
                            relief="flat", padx=20)
        send_btn.pack(side="right")
        
    def add_message(self, sender, message):
        """Add message to chat display"""
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state="normal")
        
        if sender == "L.U.F.F.Y":
            self.chat_display.insert("end", f"[{timestamp}] ", "timestamp")
            self.chat_display.insert("end", f"{sender}: ", "luffy")
            self.chat_display.insert("end", f"{message}\n\n", "message")
        else:
            self.chat_display.insert("end", f"[{timestamp}] ", "timestamp")
            self.chat_display.insert("end", f"{sender}: ", "user")
            self.chat_display.insert("end", f"{message}\n\n", "message")
        
        # Configure tags
        self.chat_display.tag_config("timestamp", foreground="#888888")
        self.chat_display.tag_config("luffy", foreground="#00ffff", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("user", foreground="#00ff00", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("message", foreground="#ffffff")
        
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
        
    def send_message(self, event=None):
        """Send message and get response"""
        message = self.input_var.get().strip()
        if not message:
            return
            
        self.add_message("You", message)
        self.input_var.set("")
        
        # Process command in separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        """Process message and get response"""
        response = self.luffy.process_command(message)
        self.add_message("L.U.F.F.Y", response)
        self.luffy.speak(response)
        
    def voice_command(self):
        """Handle voice command"""
        if not VOICE_AVAILABLE:
            self.add_message("L.U.F.F.Y", "Voice recognition not available. Please install required packages.")
            return
            
        # Update button to show listening state
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, tk.Button) and "🎤" in btn.cget("text"):
                                btn.config(text="🎤 Listening...", state="disabled")
                                break
        
        self.add_message("System", "🎤 Ready to listen - speak now...")
        
        def listen_thread():
            try:
                command = self.luffy.listen()
                if command:
                    self.add_message("You", command)
                    self.process_message(command)
                else:
                    self.add_message("System", "No voice input detected. Try speaking louder or closer to microphone.")
            finally:
                # Reset button
                for widget in self.root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Frame):
                                for btn in child.winfo_children():
                                    if isinstance(btn, tk.Button) and "Listening" in btn.cget("text"):
                                        btn.config(text="🎤 Voice", state="normal")
                                        break
                
        threading.Thread(target=listen_thread, daemon=True).start()
    
    def toggle_wake_word(self):
        """Toggle wake word listening on/off"""
        if not VOICE_AVAILABLE:
            self.add_message("L.U.F.F.Y", "Voice recognition not available. Please install required packages.")
            return
            
        if not self.luffy.wake_word_active:
            self.luffy.start_wake_word_listening()
            self.add_message("System", "👂 Wake word detection ENABLED - say 'Hey L.U.F.F.Y' anytime!")
            # Update button appearance
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button) and "👂" in btn.cget("text"):
                                    btn.config(text="👂 ACTIVE", bg="#00ff00", fg="#000000")
                                    break
        else:
            self.luffy.stop_wake_word_listening()
            self.add_message("System", "👂 Wake word detection DISABLED")
            # Reset button appearance
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button) and "ACTIVE" in btn.cget("text"):
                                    btn.config(text="👂 Wake Word", bg="#1a1a1a", fg="#00ffff")
                                    break
    
    def handle_wake_word_activation(self, event_type, wake_word, command):
        """Handle wake word activation from L.U.F.F.Y"""
        if event_type == "wake_word":
            self.add_message("System", f"👂 Wake word detected: '{wake_word}'")
            self.add_message("You", command)
            self.process_message(command)
        
    def quick_command(self, command):
        """Execute quick command"""
        self.add_message("You", command)
        threading.Thread(target=self.process_message, args=(command,), daemon=True).start()
        
    def quick_search(self):
        """Quick search dialog"""
        query = tk.simpledialog.askstring("Search", "What would you like to search for?")
        if query:
            self.quick_command(f"search {query}")
            
    def quick_calc(self):
        """Quick calculator dialog"""
        expression = tk.simpledialog.askstring("Calculator", "Enter calculation:")
        if expression:
            self.quick_command(f"calculate {expression}")
            
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    import tkinter.simpledialog
    app = LUFFYAdvancedGUI()
    app.run()
