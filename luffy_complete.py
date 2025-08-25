#!/usr/bin/env python3
"""L.U.F.F.Y - Learning Universal Friendly Framework for You
Learning Universal Friendly Framework for You - Advanced AI Assistant
"""

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
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageGrab

# Voice recognition imports
try:
    import speech_recognition as sr
    import pyaudio
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# Advanced voice synthesis imports
try:
    import edge_tts
    import asyncio
    import pygame
    import io
    ADVANCED_TTS = True
except ImportError:
    ADVANCED_TTS = False

# Vision imports
try:
    import cv2
    import pytesseract
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

# Local LLM imports
try:
    import ollama
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

class LUFFYVoiceInterface:
    """Voice Interface Module - Speech recognition and synthesis"""
    
    def __init__(self):
        self.setup_voice()
        self.wake_word_active = False
        
    def setup_voice(self):
        if VOICE_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Enhanced TTS setup with Luffy-style voice
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                
                # Try to find a young, energetic voice for Luffy
                luffy_voice = None
                for voice in voices:
                    voice_name = voice.name.lower()
                    # Look for younger, more energetic voices
                    if any(name in voice_name for name in ['david', 'mark', 'ryan', 'kevin', 'justin']):
                        luffy_voice = voice.id
                        break
                    # Fallback to any male voice
                    elif 'male' in voice_name or any(name in voice_name for name in ['george', 'paul', 'richard']):
                        luffy_voice = voice.id
                
                if luffy_voice:
                    self.tts_engine.setProperty('voice', luffy_voice)
                
                # Luffy-style speech settings - energetic and fast
                self.tts_engine.setProperty('rate', 220)  # Faster for Luffy's energy
                self.tts_engine.setProperty('volume', 1.0)  # Full volume for enthusiasm
                
                # Test microphone
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                print("Voice recognition ready with enhanced settings")
            except Exception as e:
                print(f"Voice setup failed: {e}")
    
    def listen(self, timeout=5):
        if not VOICE_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                # Faster ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                # Optimized for speed
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.5
                
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=6)
            
            # Try multiple recognition services for better accuracy
            try:
                result = self.recognizer.recognize_google(audio).lower()
                return result
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                # Fallback to Windows Speech Recognition if available
                try:
                    result = self.recognizer.recognize_sphinx(audio).lower()
                    return result
                except:
                    return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            return None
    
    def speak(self, text):
        print(f"L.U.F.F.Y: {text}")
        if ADVANCED_TTS:
            # Use advanced TTS for more natural Luffy voice
            asyncio.run(self.speak_with_edge_tts(text))
        elif VOICE_AVAILABLE:
            try:
                # Add Luffy-style vocal expressions
                luffy_text = self.add_luffy_expressions(text)
                
                # Energetic speech settings for Luffy
                self.tts_engine.setProperty('rate', 240)  # Very fast and energetic
                self.tts_engine.setProperty('volume', 1.0)  # Full volume
                
                self.tts_engine.say(luffy_text)
                self.tts_engine.runAndWait()
            except:
                pass
    
    async def speak_with_edge_tts(self, text):
        """Use Microsoft Edge TTS for more natural Luffy voice"""
        try:
            # Add Luffy expressions
            luffy_text = self.add_luffy_expressions(text)
            
            # Use a young, energetic male voice
            voice = "en-US-ChristopherNeural"  # Young, energetic male voice
            
            # Create TTS with SSML for energy and speed
            ssml_text = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="{voice}">
                    <prosody rate="fast" pitch="high" volume="loud">
                        {luffy_text}
                    </prosody>
                </voice>
            </speak>
            """
            
            communicate = edge_tts.Communicate(ssml_text, voice)
            
            # Generate audio
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            # Play audio using pygame
            if audio_data:
                pygame.mixer.init()
                audio_io = io.BytesIO(audio_data)
                pygame.mixer.music.load(audio_io)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            print(f"Advanced TTS failed: {e}, falling back to basic TTS")
            if VOICE_AVAILABLE:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
    
    def add_luffy_expressions(self, text):
        """Add Luffy-style vocal expressions and emphasis"""
        # Add excitement and energy to responses
        if any(word in text.lower() for word in ["opening", "awesome", "ready", "let's", "yosh"]):
            text = text + "!"
        
        # Replace certain words with more energetic versions
        replacements = {
            "okay": "alright",
            "yes": "yeah",
            "sure": "absolutely",
            "good": "awesome",
            "nice": "amazing"
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def start_wake_word_detection(self, callback):
        if not VOICE_AVAILABLE:
            print("Wake word detection unavailable - voice recognition not installed")
            return
            
        self.wake_word_active = True
        def wake_word_loop():
            pass  # Silent wake word detection
            while self.wake_word_active:
                try:
                    with self.microphone as source:
                        # Optimized for wake word detection
                        self.recognizer.energy_threshold = 150
                        self.recognizer.pause_threshold = 0.5
                        self.recognizer.dynamic_energy_threshold = True
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # Enhanced wake word patterns
                    wake_patterns = [
                        "hey luffy", "luffy", "hey l.u.f.f.y", "hey jarvis",
                        "okay luffy", "hi luffy", "luffy help", "luffy assistant"
                    ]
                    
                    if any(wake_phrase in text for wake_phrase in ["hey luffy", "luffy", "hey l.u.f.f.y", "l.u.f.f.y"]):
                        # Enhanced wake word responses
                        responses = [
                            "Hey Wesley! What's up?",
                            "I'm here, captain! What do you need?",
                            "Ready for our next coding adventure!",
                            "Yosh! What can I help with today?",
                            "At your service, Wesley!"
                        ]
                        import random
                        self.speak(random.choice(responses))
                        callback()
                        time.sleep(2)  # Prevent immediate re-triggering
                    elif any(wake in text for wake in wake_patterns):
                        print(f"Wake word detected: {text}")
                        responses = [
                            "Yosh Wesley! What do you need?",
                            "I'm ready! What's our coding plan today?",
                            "Alright! Let's tackle this together!",
                            "Hey Wesley! What can I help with?",
                            "Awesome! Ready to boost your Python skills?"
                        ]
                        import random
                        response = random.choice(responses)
                        self.speak(response)
                        
                        # Listen for command after wake word
                        command = self.listen(timeout=5)
                        if command:
                            callback(command)
                        else:
                            self.speak("Huh? I didn't hear you!")
                            
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue
                except Exception as e:
                    if self.wake_word_active:
                        print(f"Wake word detection error: {e}")
                        time.sleep(1)
                        continue
        threading.Thread(target=wake_word_loop, daemon=True).start()

class LUFFYVisionModule:
    """Vision Module - Screen analysis, object detection, text extraction"""
    
    def __init__(self):
        self.setup_vision()
    
    def setup_vision(self):
        pass  # Silent initialization
    
    def capture_screen(self):
        """Capture screenshot"""
        try:
            screenshot = ImageGrab.grab()
            return np.array(screenshot)
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def analyze_screen(self):
        """Analyze current screen content"""
        if not VISION_AVAILABLE:
            return "Vision module not available"
        
        screen = self.capture_screen()
        if screen is None:
            return "Could not capture screen"
        
        # Extract text from screen
        text = pytesseract.image_to_string(screen)
        
        # Basic analysis
        analysis = {
            "text_detected": len(text.strip()) > 0,
            "text_content": text[:200] + "..." if len(text) > 200 else text,
            "screen_resolution": f"{screen.shape[1]}x{screen.shape[0]}"
        }
        
        return f"Screen Analysis: Resolution {analysis['screen_resolution']}, Text detected: {analysis['text_detected']}"
    
    def find_on_screen(self, target_text):
        """Find specific text on screen"""
        if not VISION_AVAILABLE:
            return "Vision module not available"
        
        screen = self.capture_screen()
        if screen is None:
            return "Could not capture screen"
        
        text = pytesseract.image_to_string(screen)
        if target_text.lower() in text.lower():
            return f"Found '{target_text}' on screen"
        else:
            return f"'{target_text}' not found on screen"

class LUFFYBrain:
    """AI Brain Module - Local LLM integration with tool calling"""
    
    def __init__(self):
        self.setup_llm()
        self.memory = []
        
    def setup_llm(self):
        global LLM_AVAILABLE
        if LLM_AVAILABLE:
            try:
                # Check if Ollama is running and has models
                models = ollama.list()
                if models:
                    self.model = "llama3.1:latest"  # or first available model
                    print("AI Brain Ready with Local LLM")
                else:
                    print("No LLM models found - install Ollama and pull llama3.1")
                    LLM_AVAILABLE = False
            except:
                print("Ollama not available - using basic responses")
                LLM_AVAILABLE = False
    
    def process_with_llm(self, query, context=""):
        """Process query using local LLM"""
        if not LLM_AVAILABLE:
            return self.enhanced_response(query)
        
        try:
            prompt = f"Context: {context}\nUser: {query}\nAssistant:"
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except:
            return self.enhanced_response(query)
    
    def enhanced_response(self, query):
        """Enhanced responses with personality when LLM unavailable"""
        query = query.lower()
        
        # Greetings with Luffy personality
        if any(word in query for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            greetings = [
                "Hey there! I'm Luffy! What adventure are we going on?",
                "Yo! Ready for some fun?",
                "Hi! Let's do something awesome together!",
                "Hey! I'm super excited to help you out!",
                "Yosh! What cool stuff are we gonna do today?"
            ]
            import random
            return random.choice(greetings)
        
        # Time queries
        elif "time" in query:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            return f"It's {current_time} right now! Time flies when you're having adventures!"
        
        # Date queries
        elif "date" in query or "today" in query:
            current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
            return f"Today is {current_date}! What are we gonna do today?"
        
        # Weather (placeholder)
        elif "weather" in query:
            return "I wish I could check the weather for our next adventure! Weather integration is ready for setup!"
        
        # Personal questions
        elif any(word in query for word in ["who are you", "what are you", "your name"]):
            return "I'm Luffy! I'm gonna be the King of the Pirates... I mean, your awesome AI assistant! I can do tons of cool stuff!"
        
        # Capabilities
        elif any(word in query for word in ["what can you do", "help me", "capabilities"]):
            return "I can do so many things! Open apps, search the web, control your computer, and tons more! Just tell me what you want - I'm super strong... I mean, super helpful!"
        
        # Jokes
        elif "joke" in query or "funny" in query:
            jokes = [
                "Why did the rubber band break? Because it stretched too far! Get it? Like my powers! Shishishi!",
                "What's a pirate's favorite letter? You'd think it's R, but it's actually the C! Shishishi!",
                "Why don't computers ever get hungry? Because they always have bytes! That's so funny!",
                "What do you call a sleeping bull? A bulldozer! Ahaha, that's awesome!",
                "Why did the scarecrow win an award? He was outstanding in his field! Just like me!"
            ]
            import random
            return random.choice(jokes)
        
        # Thanks
        elif any(word in query for word in ["thank", "thanks", "appreciate"]):
            responses = [
                "No problem! That was fun!",
                "Yosh! Anytime!",
                "Awesome! I love helping out!",
                "That was easy! What's next?",
                "Shishishi! You got it!"
            ]
            import random
            return random.choice(responses)
        
        # Default response
        else:
            defaults = [
                "What do you wanna do? I'm ready for anything!",
                "Let's go! What's the plan?",
                "I'm pumped! What can I help with?",
                "Yosh! Tell me what you need!",
                "This is gonna be awesome! What should we do?"
            ]
            import random
            return random.choice(defaults)

class SystemControl:
    """System Control Module - Application, file, web, and hardware control"""
    
    def __init__(self):
        print("System Control Ready")
    
    def execute_system_command(self, command):
        """Execute system-level commands"""
        command = command.lower()
        
        if "shutdown" in command:
            subprocess.run(["shutdown", "/s", "/t", "30"])
            return "System shutdown initiated"
        elif "restart" in command:
            subprocess.run(["shutdown", "/r", "/t", "30"])
            return "System restart initiated"
        elif "lock" in command:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return "System locked"
        elif "volume up" in command:
            subprocess.run(["nircmd.exe", "changesysvolume", "5000"])
            return "Volume increased"
        elif "volume down" in command:
            subprocess.run(["nircmd.exe", "changesysvolume", "-5000"])
            return "Volume decreased"
        
        return "System command not recognized"
    
    def __init__(self):
        print("System Control Ready")
        self.app_cache = {}  # Cache for faster app discovery
        self.cache_time = 0
        
    def discover_applications(self):
        """Fast application discovery with caching"""
        # Use cache if less than 5 minutes old
        current_time = time.time()
        if self.app_cache and (current_time - self.cache_time) < 300:
            return self.app_cache
            
        apps = {}
        
        # Built-in Windows applications (instant)
        system_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe", 
            "paint": "mspaint.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "registry editor": "regedit.exe",
            "device manager": "devmgmt.msc",
            "disk management": "diskmgmt.msc",
            "services": "services.msc",
            "event viewer": "eventvwr.exe",
            "system configuration": "msconfig.exe",
            "windows explorer": "explorer.exe"
        }
        apps.update(system_apps)
        
        # Windows Store apps (instant)
        store_apps = {
            "netflix": "netflix:",
            "spotify": "spotify:",
            "whatsapp": "whatsapp:",
            "disney plus": "disneyplus:",
            "prime video": "primevideo:",
            "microsoft store": "ms-windows-store:",
            "xbox": "xbox:",
            "mail": "outlookmail:",
            "calendar": "outlookcal:",
            "photos": "ms-photos:",
            "movies & tv": "mswindowsvideo:",
            "groove music": "mswindowsmusic:",
            "maps": "bingmaps:",
            "weather": "bingweather:",
            "news": "bingnews:",
            "microsoft edge": "microsoft-edge:",
            "settings": "ms-settings:",
            "calculator": "calculator:",
            "camera": "microsoft.windows.camera:",
            "voice recorder": "ms-sound-recorder:"
        }
        apps.update(store_apps)
        
        # Add specific browser paths first for faster detection
        browser_paths = [
            (r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "brave"),
            (r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe", "brave"),
            (os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"), "brave"),
            (r"C:\Program Files\Google\Chrome\Application\chrome.exe", "chrome"),
            (r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "chrome"),
            (r"C:\Program Files\Mozilla Firefox\firefox.exe", "firefox"),
            (r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe", "firefox"),
            (r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", "edge")
        ]
        
        for path, name in browser_paths:
            if os.path.exists(path):
                apps[name] = path
        
        # Fast search - essential paths
        search_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.path.expanduser("~\\AppData\\Local"),
            r"C:\Program Files\ASUS",
            r"C:\Program Files (x86)\ASUS"
        ]
        
        # Scan all directories for executable files
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path):
                        # Skip system directories that might cause issues
                        skip_dirs = ['system32', 'syswow64', 'winsxs', 'temp', 'cache', '$recycle.bin']
                        if any(skip_dir in root.lower() for skip_dir in skip_dirs):
                            continue
                            
                        depth = root[len(search_path):].count(os.sep)
                        if depth > 2:  # Reduced depth for speed
                            continue
                            
                        for file in files:
                            if file.lower().endswith('.exe'):  # Only .exe for speed
                                try:
                                    file_lower = file.lower()
                                    app_name = file_lower.replace('.exe', '')
                                    
                                    # Skip system files and installers quickly
                                    skip_files = ['uninstall', 'setup', 'install', 'update', 'patch']
                                    if not any(skip in app_name for skip in skip_files):
                                        full_path = os.path.join(root, file)
                                        apps[app_name] = full_path
                                        
                                        # Quick alternative names for common apps
                                        if 'chrome' in app_name:
                                            apps['chrome'] = full_path
                                        elif 'firefox' in app_name:
                                            apps['firefox'] = full_path
                                        elif 'whatsapp' in app_name:
                                            apps['whatsapp'] = full_path
                                        elif 'discord' in app_name:
                                            apps['discord'] = full_path
                                        elif 'spotify' in app_name:
                                            apps['spotify'] = full_path
                                        elif 'armoury' in app_name or 'armory' in app_name:
                                            apps['armoury crate'] = full_path
                                except (OSError, PermissionError):
                                    continue
                except (OSError, PermissionError):
                    continue
        
        # Cache the results for faster future access
        self.app_cache = apps
        self.cache_time = current_time
        
        return apps
    
    def open_application(self, app_name):
        """Open applications with enhanced discovery"""
        if not app_name:
            return "Please specify an application name."
        
        app_name = app_name.lower().strip()
        
        # Get available apps
        apps = self.discover_applications()
        
        # Direct match
        if app_name in apps:
            try:
                app_path = apps[app_name]
                
                # Handle different app types
                if app_path.startswith(('http://', 'https://', 'ms-', 'netflix:', 'spotify:', 'whatsapp:')):
                    # Protocol or URL launch
                    subprocess.run(['start', app_path], shell=True)
                    return f"Opening {app_name}..."
                elif app_path.endswith('.lnk'):
                    # Shortcut file
                    subprocess.run(['start', '', app_path], shell=True)
                    return f"Opening {app_name}..."
                else:
                    # Regular executable
                    subprocess.Popen(app_path, shell=True)
                    return f"Opening {app_name}..."
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"
        
        # Improved partial match search with better scoring
        matches = []
        for app, path in apps.items():
            score = 0
            app_words = app.lower().split()
            search_words = app_name.split()
            
            # Exact match gets highest score
            if app_name == app:
                score = 1000
            # Check if all search words are in app name
            elif all(word in app for word in search_words):
                score = 500 + len([w for w in search_words if w in app_words])
            # Check if any search word matches app words
            elif any(word in app_words for word in search_words):
                score = 100 + len([w for w in search_words if w in app_words])
            # Basic substring match
            elif app_name in app or app in app_name:
                score = 50
            
            if score > 0:
                matches.append((app, path, score))
        
        if matches:
            # Use best match based on score, then shortest name
            best_match = max(matches, key=lambda x: (x[2], -len(x[0])))
            app, path, score = best_match
            
            try:
                if path.startswith(('http://', 'https://', 'ms-', 'netflix:', 'spotify:', 'whatsapp:')):
                    subprocess.run(['start', path], shell=True)
                elif path.endswith('.lnk'):
                    subprocess.run(['start', '', path], shell=True)
                else:
                    subprocess.Popen(path, shell=True)
                return f"Opening {app}..."
            except Exception as e:
                return f"Failed to open {app}: {str(e)}"
        
        # If no match found, show available options
        app_list = list(apps.keys())[:20]  # Show first 20 apps
        return f"Application '{app_name}' not found. Available apps include: {', '.join(app_list)}..."
        
        # Try Windows Start command as fallback
        try:
            subprocess.run(["start", "", app_name], shell=True)
            return f"Attempting to open {app_name} via Windows Start"
        except:
            return f"Could not find application '{app_name}'. Try being more specific or check if it's installed."
    
    def get_system_info(self):
        """Get system information"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"System Status - CPU: {cpu}%, Memory: {memory.percent}%, Disk: {disk.percent}%"
        except:
            return "Could not retrieve system information"

class LUFFYInternetModule:
    """Internet Module - Web search, APIs, real-time data"""
    
    def __init__(self):
        print("Internet Module Ready")
    
    def web_search(self, query):
        """Perform web search"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for: {query}"
        except:
            return "Web search failed"
    
    def get_weather(self, city="London"):
        """Get weather information"""
        try:
            # This would require an API key in real implementation
            return f"Weather information for {city} - please add API key for live data"
        except:
            return "Weather service unavailable"
    
    def get_news(self):
        """Get latest news"""
        try:
            # This would require news API integration
            return "Latest news - please configure news API for live updates"
        except:
            return "News service unavailable"

class LUFFYDashboard:
    """Dashboard Module - GUI interface, status monitoring, command log"""
    
    def __init__(self):
        self.setup_gui()
        self.setup_modules()
        
    def setup_modules(self):
        """Initialize all system modules"""
        self.voice = LUFFYVoiceInterface()
        self.vision = LUFFYVisionModule()
        self.ai_brain = LUFFYBrain()
        self.system_control = SystemControl()
        self.internet = LUFFYInternetModule()
        
        # Set up voice callback
        self.voice.start_wake_word_detection(self.process_voice_command)
    
    def setup_gui(self):
        """Setup main dashboard interface"""
        self.root = tk.Tk()
        self.root.title("L.U.F.F.Y - AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")
        
        self.setup_header()
        self.setup_main_interface()
        self.setup_control_panel()
        self.setup_status_bar()
        
    def setup_header(self):
        """Setup header with L.U.F.F.Y branding"""
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill="x", padx=10, pady=5)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="🤖 L.U.F.F.Y AI Assistant", font=("Arial", 16, "bold"), bg="#1a1a1a", fg="#00ff00")
        title_label.pack(side="left", pady=20)
        
        subtitle = tk.Label(header, text="Learning Universal Friendly Framework for You", 
                           font=("Arial", 12), 
                           fg="#87CEEB", bg="#000000")
        subtitle.pack(side="left", padx=(10, 0), pady=25)
    
    def setup_main_interface(self):
        """Setup main chat and display area"""
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=100, height=25,
            font=("Consolas", 11), bg="#001122", fg="#00FFFF",
            insertbackground="#00FFFF", selectbackground="#003366"
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg="#000000", height=40)
        input_frame.pack(fill="x", pady=5)
        input_frame.pack_propagate(False)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                   font=("Arial", 12), bg="#001122", fg="#00FFFF",
                                   insertbackground="#00FFFF")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message,
                            bg="#00BFFF", fg="#000000", font=("Arial", 10, "bold"))
        send_btn.pack(side="right")
    
    def setup_control_panel(self):
        """Setup control panel with module buttons"""
        control_frame = tk.Frame(self.root, bg="#000000", height=60)
        control_frame.pack(fill="x", padx=10, pady=5)
        control_frame.pack_propagate(False)
        
        buttons = [
            ("Voice", self.process_voice_command),
            ("Vision", self.vision_analysis),
            ("AI Brain", self.ai_query),
            ("System", self.system_command),
            ("Web", self.web_command),
            ("Status", self.show_status)
        ]
        
        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                           bg="#001122", fg="#00BFFF", font=("Arial", 10),
                           padx=15, pady=5)
            btn.pack(side="left", padx=2)
    
    def setup_status_bar(self):
        """Setup status monitoring bar"""
        status_frame = tk.Frame(self.root, bg="#000000", height=30)
        status_frame.pack(fill="x", padx=10, pady=2)
        status_frame.pack_propagate(False)
        
        voice_status = "VOICE ON" if VOICE_AVAILABLE else "VOICE OFF"
        vision_status = "VISION ON" if VISION_AVAILABLE else "VISION OFF"
        llm_status = "LLM ON" if LLM_AVAILABLE else "LLM OFF"
        
        self.status_label = tk.Label(status_frame, 
                                    text=f"● ONLINE | {voice_status} | {vision_status} | {llm_status}",
                                    font=("Arial", 10), fg="#00FF00", bg="#000000")
        self.status_label.pack(side="left")
        
        # System info
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            sys_info = f"CPU: {cpu}% | RAM: {memory}%"
        except:
            sys_info = "System info unavailable"
            
        self.sys_info_label = tk.Label(status_frame, text=sys_info,
                                      font=("Arial", 10), fg="#87CEEB", bg="#000000")
        self.sys_info_label.pack(side="right")
    
    def add_message(self, sender, message, color="#00FFFF"):
        """Add message to chat display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
    
    def send_message(self):
        """Send message from input field"""
        message = self.input_var.get().strip()
        if message:
            self.add_message("User", message)
            self.input_var.set("")
            
            # Process command
            threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def process_command(self, command):
        """Process user command through appropriate module - optimized for speed"""
        command_lower = command.lower().strip()
        
        # Voice shortcuts and aliases
        if any(phrase in command_lower for phrase in ["open", "launch", "start", "run"]):
            app_name = command_lower
            for word in ["open", "launch", "start", "run"]:
                app_name = app_name.replace(word, "").strip()
            response = self.system_control.open_application(app_name)
            
        # YouTube Music commands
        elif any(phrase in command_lower for phrase in ["play youtube music", "youtube music", "open youtube music"]):
            # Check if Brave is available
            apps = self.system_control.discover_applications()
            if "brave" in apps:
                try:
                    subprocess.Popen([apps["brave"], "https://music.youtube.com"])
                    response = "Yosh! Opening YouTube Music in Brave!"
                except:
                    response = "Couldn't open YouTube Music in Brave!"
            else:
                # Fallback to default browser
                import webbrowser
                webbrowser.open("https://music.youtube.com")
                response = "Opening YouTube Music in your default browser!"
                
        # Specific browser + site commands
        elif "from brave" in command_lower or "in brave" in command_lower:
            apps = self.system_control.discover_applications()
            if "brave" in apps:
                if "youtube" in command_lower:
                    if "music" in command_lower:
                        url = "https://music.youtube.com"
                        site_name = "YouTube Music"
                    else:
                        url = "https://youtube.com"
                        site_name = "YouTube"
                elif "netflix" in command_lower:
                    url = "https://netflix.com"
                    site_name = "Netflix"
                elif "spotify" in command_lower:
                    url = "https://open.spotify.com"
                    site_name = "Spotify"
                else:
                    url = "https://google.com"
                    site_name = "Google"
                
                try:
                    subprocess.Popen([apps["brave"], url])
                    response = f"Awesome! Opening {site_name} in Brave!"
                except:
                    response = f"Couldn't open {site_name} in Brave!"
            else:
                response = "Brave browser not found! Want me to find it?"
            
        elif any(phrase in command_lower for phrase in ["search for", "google", "find", "look up"]):
            query = command_lower
            for phrase in ["search for", "search", "google", "find", "look up"]:
                query = query.replace(phrase, "").strip()
            response = self.internet.web_search(query)
            
        elif any(phrase in command_lower for phrase in ["analyze screen", "screen analysis", "what's on screen", "see screen"]):
            response = self.vision.analyze_screen()
            
        elif any(phrase in command_lower for phrase in ["system status", "system info", "how's the system", "computer status"]):
            response = self.system_control.get_system_info()
            
        elif any(phrase in command_lower for phrase in ["shutdown", "restart", "reboot", "lock", "sleep", "volume up", "volume down", "mute"]):
            response = self.system_control.execute_system_command(command)
            
        # Natural language commands with Luffy personality
        elif any(phrase in command_lower for phrase in ["what time", "current time", "time is it"]):
            response = f"It's {datetime.datetime.now().strftime('%I:%M %p')} right now! Time for adventure!"
            
        elif any(phrase in command_lower for phrase in ["what date", "today's date", "what day"]):
            response = f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}! What awesome stuff are we gonna do?"
            
        elif any(phrase in command_lower for phrase in ["tell me a joke", "make me laugh", "something funny"]):
            jokes = [
                "Why did the rubber band break? Because it stretched too far! Like my powers! Shishishi!",
                "What's a pirate's favorite letter? You'd think it's R, but it's actually the C! Shishishi!",
                "Why don't computers get hungry? They always have bytes! That's so funny!"
            ]
            import random
            response = random.choice(jokes)
            
        else:
            # Use AI Brain for general queries
            response = self.ai_brain.process_with_llm(command)
        
        self.add_message("L.U.F.F.Y", response)
        self.voice.speak(response)
    
    def process_voice_command(self, command=None):
        """Process voice command from wake word detection or manual input"""
        if not command:
            command = self.voice.listen(timeout=8)
        
        if command:
            self.add_message("You", command)
            # Route through unified command handler (handles messaging + TTS)
            self.process_command(command)
        # No system message for failed voice input
    
    def vision_analysis(self):
        """Perform vision analysis"""
        self.add_message("System", "Analyzing screen...")
        result = self.vision.analyze_screen()
        self.add_message("Vision", result)
    
    def ai_query(self):
        """Direct AI query"""
        query = tk.simpledialog.askstring("AI Query", "Ask the AI:")
        if query:
            response = self.ai_brain.process_with_llm(query)
            self.add_message("AI Brain", response)
    
    def system_command(self):
        """System command dialog"""
        cmd = tk.simpledialog.askstring("System Command", "Enter system command:")
        if cmd:
            response = self.system_control.execute_system_command(cmd)
            self.add_message("System", response)
    
    def web_command(self):
        """Web search dialog"""
        query = tk.simpledialog.askstring("Web Search", "Search for:")
        if query:
            response = self.internet.web_search(query)
            self.add_message("Web", response)
    
    def show_status(self):
        """Show detailed system status"""
        status = f"""
L.U.F.F.Y System Status:
- Voice Interface: {'Active' if VOICE_AVAILABLE else 'Inactive'}
- Vision Module: {'Active' if VISION_AVAILABLE else 'Inactive'}
- AI Brain (LLM): {'Active' if LLM_AVAILABLE else 'Inactive'}
- System Control: Active
- Internet Module: Active
- Dashboard: Active
        """
        self.add_message("Status", status.strip())
    
    def run(self):
        """Start the L.U.F.F.Y system"""
        self.add_message("System", "L.U.F.F.Y Complete System initialized. All modules online!")
        self.voice.speak("Hey Wesley! L.U.F.F.Y is ready to help you become the coding king you're meant to be! What's our mission today?")
        self.root.mainloop()

if __name__ == "__main__":
    import tkinter.simpledialog
    
    luffy = LUFFYDashboard()
    luffy.run()
