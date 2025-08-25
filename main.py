"""
L.U.F.F.Y - Learning Universal Friendly Framework for You
An intelligent AI assistant with advanced learning capabilities
"""

# Import speech recognition with error handling for Python 3.13
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("Speech recognition not available - using text input only")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Text-to-speech not available - using text output only")
import datetime
import webbrowser
import os
import requests
import json
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import queue
import time
import re
import math
import random
from ai_brain import AIBrain

class LUFFY:
    def __init__(self):
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            except:
                SPEECH_AVAILABLE = False
                print("Microphone not available - using text input only")
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.setup_voice()
            except:
                TTS_AVAILABLE = False
                print("Text-to-speech not available - using text output only")
        self.listening = False
        self.command_queue = queue.Queue()
        
        # Initialize AI Brain
        self.brain = AIBrain()
        self.conversation_context = {}
        
        # Import task automation
        from task_automation import TaskAutomation
        self.task_manager = TaskAutomation()
        
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
        
    def setup_voice(self):
        """Configure the text-to-speech engine"""
        if not TTS_AVAILABLE:
            return
        
        try:
            voices = self.tts_engine.getProperty('voices')
            # Try to find a male voice
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_engine.setProperty('rate', 180)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
        except:
            print("Voice setup failed - using default settings")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"L.U.F.F.Y: {text}")
        if TTS_AVAILABLE:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass  # Just print if TTS fails
    
    def listen(self):
        """Listen for voice commands"""
        if not SPEECH_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except:
            return None  # Simplified error handling
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        return now.strftime("The current time is %I:%M %p, sir.")
    
    def get_current_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        return now.strftime("Today is %A, %B %d, %Y.")
    
    def calculate(self, expression):
        """Perform mathematical calculations"""
        try:
            # Clean the expression
            expression = expression.replace('x', '*').replace('÷', '/')
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"The answer is {result}, sir."
            else:
                return "I can only perform basic mathematical operations, sir."
        except:
            return "I couldn't calculate that, sir. Please check your expression."
    
    def search_web(self, query):
        """Search the web"""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"I've opened a web search for '{query}' in your browser, sir."
    
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
        """Process and execute commands with AI intelligence"""
        if not command:
            return
        
        original_command = command
        command = command.lower()
        
        # Check for intelligent contextual response first
        contextual_response = self.brain.get_contextual_response(command)
        if contextual_response:
            self.speak(contextual_response)
            self.brain.add_to_memory(original_command, contextual_response, self.conversation_context)
            return True
        
        # Greetings with AI enhancement
        if any(word in command for word in ['hello', 'hi', 'hey', 'luffy']):
            # Check for personalized greeting
            personalized = self.brain.generate_personalized_response(command, self.brain.get_recent_context(), 'formal')
            if personalized:
                response = personalized
            else:
                response = random.choice(self.greetings).replace('sir', 'captain')
                # Add smart suggestions
                suggestions = self.brain.get_smart_suggestions()
                if suggestions:
                    response += " " + suggestions[0]
            
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Time queries
        elif 'time' in command:
            response = self.get_current_time()
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Date queries
        elif 'date' in command or 'today' in command:
            response = self.get_current_date()
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Calculations with learning
        elif any(word in command for word in ['calculate', 'compute', 'math', '+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            # Extract mathematical expression
            math_pattern = r'[\d+\-*/().]+|plus|minus|times|divided by'
            expression = ' '.join(re.findall(math_pattern, command))
            expression = expression.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
            if expression:
                response = self.calculate(expression)
                # Check if user frequently does calculations
                if self.brain.user_profile.get('command_frequency', {}).get('calculation', 0) > 5:
                    response += " I notice you do calculations often. I'm always ready for math, captain."
            else:
                response = "Please provide a mathematical expression, captain."
            
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Web search with intelligence
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            if query:
                response = self.search_web(query)
                # Remember search topics
                self.conversation_context['last_search'] = query
            else:
                response = "What would you like me to search for, captain?"
            
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Open applications with learning
        elif 'open' in command:
            app = command.replace('open', '').strip()
            response = self.open_application(app)
            # Remember frequently used apps
            self.conversation_context['last_app'] = app
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Weather with learning
        elif 'weather' in command:
            response = "I would need a weather API key to provide weather information, captain. However, I can remember your weather preferences for future updates."
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Exit commands with memory save
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            # Save learned data
            self.brain.save_brain_data()
            
            # Personalized goodbye
            total_interactions = self.brain.user_profile.get('total_interactions', 0)
            if total_interactions > 20:
                response = "Goodbye, captain. I've learned much from our conversations today. Until next time."
            else:
                response = "Goodbye, captain. It was a pleasure serving you."
            
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
            return False
        
        # Learning and memory commands
        elif 'remember' in command or 'learn' in command:
            if 'remember' in command:
                info = command.replace('remember', '').strip()
                self.brain.set_user_preference('remembered_info', info)
                response = f"I'll remember that, captain: {info}"
            else:
                response = "I'm always learning from our interactions, captain."
            
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Memory summary
        elif 'what do you know' in command or 'memory' in command:
            summary = self.brain.get_memory_summary()
            response = f"I've had {summary['total_interactions']} interactions with you, learned {summary['learned_patterns']} patterns, and have {summary['preferences_set']} preferences stored, captain."
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        # Unknown command with learning
        else:
            # Analyze sentiment to provide appropriate response
            sentiment = self.brain.analyze_sentiment(command)
            if sentiment == 'negative':
                responses = [
                    "I sense frustration, captain. Let me try to help better.",
                    "I apologize for the confusion, captain. Could you rephrase that?"
                ]
            else:
                responses = [
                    "I'm not sure I understand that command, captain. I'm still learning.",
                    "Could you please rephrase that, captain? I'll remember for next time.",
                    "I didn't quite catch that, captain. Help me learn by rephrasing."
                ]
            
            response = random.choice(responses)
            self.speak(response)
            self.brain.add_to_memory(original_command, response, self.conversation_context)
        
        return True
    
    def run(self):
        """Main execution loop"""
        self.speak("L.U.F.F.Y online. Ready to assist you, captain.")
        
        while True:
            try:
                command = self.listen()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                self.speak("Shutting down, sir.")
                break

if __name__ == "__main__":
    luffy = LUFFY()
    luffy.run()
