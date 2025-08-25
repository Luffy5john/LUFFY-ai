"""
JARVIS AI Brain - Advanced Intelligence Module
Provides conversation memory, learning, and sophisticated NLP capabilities
"""

import json
import os
import datetime
import re
from collections import defaultdict, deque
import pickle
import hashlib

class AIBrain:
    def __init__(self, data_dir="jarvis_data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
        
        # Memory systems
        self.conversation_memory = deque(maxlen=100)  # Recent conversations
        self.user_preferences = {}
        self.learned_patterns = defaultdict(list)
        self.context_stack = []
        self.user_profile = {}
        
        # Load existing data
        self.load_brain_data()
        
        # Sentiment keywords
        self.positive_words = ['good', 'great', 'excellent', 'awesome', 'perfect', 'love', 'like', 'happy', 'pleased']
        self.negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated', 'annoyed']
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_brain_data(self):
        """Load saved brain data"""
        try:
            # Load user preferences
            pref_file = os.path.join(self.data_dir, "preferences.json")
            if os.path.exists(pref_file):
                with open(pref_file, 'r') as f:
                    self.user_preferences = json.load(f)
            
            # Load user profile
            profile_file = os.path.join(self.data_dir, "user_profile.json")
            if os.path.exists(profile_file):
                with open(profile_file, 'r') as f:
                    self.user_profile = json.load(f)
            
            # Load learned patterns
            patterns_file = os.path.join(self.data_dir, "patterns.pkl")
            if os.path.exists(patterns_file):
                with open(patterns_file, 'rb') as f:
                    self.learned_patterns = pickle.load(f)
                    
        except Exception as e:
            print(f"Error loading brain data: {e}")
    
    def save_brain_data(self):
        """Save brain data to files"""
        try:
            # Save preferences
            with open(os.path.join(self.data_dir, "preferences.json"), 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
            
            # Save user profile
            with open(os.path.join(self.data_dir, "user_profile.json"), 'w') as f:
                json.dump(self.user_profile, f, indent=2)
            
            # Save patterns
            with open(os.path.join(self.data_dir, "patterns.pkl"), 'wb') as f:
                pickle.dump(dict(self.learned_patterns), f)
                
        except Exception as e:
            print(f"Error saving brain data: {e}")
    
    def add_to_memory(self, user_input, jarvis_response, context=None):
        """Add interaction to conversation memory"""
        memory_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_input': user_input,
            'jarvis_response': jarvis_response,
            'context': context or {},
            'sentiment': self.analyze_sentiment(user_input)
        }
        self.conversation_memory.append(memory_entry)
        
        # Learn from this interaction
        self.learn_from_interaction(user_input, jarvis_response)
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        text = text.lower()
        positive_score = sum(1 for word in self.positive_words if word in text)
        negative_score = sum(1 for word in self.negative_words if word in text)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def learn_from_interaction(self, user_input, jarvis_response):
        """Learn patterns from user interactions"""
        # Extract keywords and patterns
        words = re.findall(r'\b\w+\b', user_input.lower())
        
        # Learn command patterns
        if len(words) > 1:
            pattern_key = ' '.join(words[:2])  # First two words as pattern
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = []
            self.learned_patterns[pattern_key].append({
                'full_command': user_input,
                'response_type': self.classify_response(jarvis_response),
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        # Update user profile
        self.update_user_profile(user_input)
    
    def classify_response(self, response):
        """Classify the type of response given"""
        response_lower = response.lower()
        if any(word in response_lower for word in ['time', 'clock']):
            return 'time_query'
        elif any(word in response_lower for word in ['calculate', 'answer', 'result']):
            return 'calculation'
        elif any(word in response_lower for word in ['search', 'google', 'browser']):
            return 'web_search'
        elif any(word in response_lower for word in ['opening', 'launched']):
            return 'app_launch'
        else:
            return 'general'
    
    def update_user_profile(self, user_input):
        """Update user profile based on interactions"""
        # Track command frequency
        if 'command_frequency' not in self.user_profile:
            self.user_profile['command_frequency'] = defaultdict(int)
        
        command_type = self.extract_command_type(user_input)
        self.user_profile['command_frequency'][command_type] += 1
        
        # Track time patterns
        current_hour = datetime.datetime.now().hour
        if 'usage_hours' not in self.user_profile:
            self.user_profile['usage_hours'] = defaultdict(int)
        self.user_profile['usage_hours'][str(current_hour)] += 1
        
        # Update last interaction
        self.user_profile['last_interaction'] = datetime.datetime.now().isoformat()
        self.user_profile['total_interactions'] = self.user_profile.get('total_interactions', 0) + 1
    
    def extract_command_type(self, user_input):
        """Extract the type of command from user input"""
        user_input = user_input.lower()
        if any(word in user_input for word in ['time', 'clock']):
            return 'time'
        elif any(word in user_input for word in ['calculate', 'math', '+', '-', '*', '/']):
            return 'calculation'
        elif any(word in user_input for word in ['search', 'google', 'find']):
            return 'search'
        elif any(word in user_input for word in ['open', 'launch', 'start']):
            return 'app_launch'
        elif any(word in user_input for word in ['weather', 'temperature']):
            return 'weather'
        else:
            return 'general'
    
    def get_contextual_response(self, user_input):
        """Generate contextual response based on memory and learning"""
        # Check recent conversation context
        recent_context = self.get_recent_context()
        
        # Check for learned patterns
        words = re.findall(r'\b\w+\b', user_input.lower())
        if len(words) >= 2:
            pattern_key = ' '.join(words[:2])
            if pattern_key in self.learned_patterns:
                # User has used similar commands before
                return self.generate_learned_response(pattern_key)
        
        # Check user preferences
        preferred_response_style = self.user_preferences.get('response_style', 'formal')
        
        # Generate personalized response
        return self.generate_personalized_response(user_input, recent_context, preferred_response_style)
    
    def get_recent_context(self):
        """Get context from recent conversations"""
        if len(self.conversation_memory) < 2:
            return None
        
        recent = list(self.conversation_memory)[-3:]  # Last 3 interactions
        return {
            'recent_topics': [entry['context'] for entry in recent if entry.get('context')],
            'recent_sentiment': [entry['sentiment'] for entry in recent],
            'recent_commands': [self.extract_command_type(entry['user_input']) for entry in recent]
        }
    
    def generate_learned_response(self, pattern_key):
        """Generate response based on learned patterns"""
        patterns = self.learned_patterns[pattern_key]
        most_recent = max(patterns, key=lambda x: x['timestamp'])
        
        response_type = most_recent['response_type']
        
        learned_responses = {
            'time_query': "I notice you often ask about time. The current time is available, sir.",
            'calculation': "Based on your calculation history, I'm ready to compute that for you, sir.",
            'web_search': "I see you frequently search for information. I'll open that search for you, sir.",
            'app_launch': "You regularly use this application. Opening it now, sir."
        }
        
        return learned_responses.get(response_type, "I remember you've asked something similar before, sir.")
    
    def generate_personalized_response(self, user_input, context, style):
        """Generate personalized response based on user profile"""
        # Get user's most common command type
        if 'command_frequency' in self.user_profile:
            most_used = max(self.user_profile['command_frequency'].items(), key=lambda x: x[1])[0]
        else:
            most_used = 'general'
        
        # Personalized greetings based on usage patterns
        if any(word in user_input.lower() for word in ['hello', 'hi', 'hey']):
            total_interactions = self.user_profile.get('total_interactions', 0)
            if total_interactions > 50:
                return "Welcome back, sir. I've learned quite a bit about your preferences."
            elif total_interactions > 10:
                return "Good to see you again, sir. How may I assist you today?"
            else:
                return "Hello, sir. I'm still learning your preferences."
        
        # Context-aware responses
        if context and context['recent_sentiment']:
            if context['recent_sentiment'][-1] == 'negative':
                return "I sense you might be frustrated, sir. Let me help resolve this quickly."
            elif context['recent_sentiment'][-1] == 'positive':
                return "I'm glad to see you're in good spirits, sir. What can I do for you?"
        
        return None  # No specific personalized response
    
    def get_smart_suggestions(self):
        """Provide smart suggestions based on usage patterns"""
        suggestions = []
        
        # Time-based suggestions
        current_hour = datetime.datetime.now().hour
        if 'usage_hours' in self.user_profile:
            if str(current_hour) in self.user_profile['usage_hours']:
                if current_hour < 12:
                    suggestions.append("Good morning, sir. Would you like me to check your schedule?")
                elif current_hour < 18:
                    suggestions.append("Good afternoon, sir. Perhaps you'd like to check the weather?")
                else:
                    suggestions.append("Good evening, sir. Shall I help you wrap up today's tasks?")
        
        # Command-based suggestions
        if 'command_frequency' in self.user_profile:
            most_used = max(self.user_profile['command_frequency'].items(), key=lambda x: x[1])
            if most_used[0] == 'calculation':
                suggestions.append("I notice you use calculations frequently. I'm ready for math problems.")
            elif most_used[0] == 'search':
                suggestions.append("You often search for information. What would you like to research today?")
        
        return suggestions
    
    def set_user_preference(self, key, value):
        """Set user preference"""
        self.user_preferences[key] = value
        self.save_brain_data()
    
    def get_user_preference(self, key, default=None):
        """Get user preference"""
        return self.user_preferences.get(key, default)
    
    def get_memory_summary(self):
        """Get summary of learned information"""
        summary = {
            'total_interactions': self.user_profile.get('total_interactions', 0),
            'learned_patterns': len(self.learned_patterns),
            'preferences_set': len(self.user_preferences),
            'memory_entries': len(self.conversation_memory)
        }
        
        if 'command_frequency' in self.user_profile:
            summary['most_used_command'] = max(
                self.user_profile['command_frequency'].items(), 
                key=lambda x: x[1]
            )[0]
        
        return summary
