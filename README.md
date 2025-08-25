# L.U.F.F.Y - Learning Universal Friendly Framework for You

An intelligent AI assistant with advanced learning capabilities. This project combines voice recognition, natural language processing, conversation memory, and adaptive learning to create your own personal AI companion.

## Features

- **Voice Recognition**: Listens to your voice commands using speech recognition
- **Text-to-Speech**: Responds with a friendly AI voice
- **Advanced AI Brain**: Learns from conversations and remembers preferences
- **Conversation Memory**: Maintains context across interactions
- **Sentiment Analysis**: Understands emotional context in commands
- **Task Automation**: Intelligent task management and reminders
- **GUI Interface**: Modern dark-themed interface with real-time chat
- **Core Capabilities**:
  - Time and date queries
  - Mathematical calculations with learning
  - Web searches with context memory
  - Application launching with usage tracking
  - Personal memory and preference storage
  - Conversational responses with adaptive personality

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install PyAudio** (for microphone access):
   - On Windows: `pip install pyaudio`
   - If you encounter issues, download the appropriate wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## Usage

### Command Line Version
```bash
python main.py
```

### GUI Version (Recommended)
```bash
python gui.py
```

## Voice Commands

- **Greetings**: "Hello L.U.F.F.Y", "Hi", "Hey"
- **Time**: "What time is it?", "Current time"
- **Date**: "What's the date?", "What day is today?"
- **Calculations**: "Calculate 15 plus 25", "What's 100 divided by 4?"
- **Web Search**: "Search for Python tutorials", "Google latest news"
- **Applications**: "Open notepad", "Open calculator", "Open browser"
- **Memory Commands**: "Remember that I like coffee", "What do you know about me?"
- **Learning**: "Learn from this", "What have you learned?"
- **Exit**: "Goodbye", "Exit", "Quit"

## Features Overview

### Voice Recognition
- Uses Google Speech Recognition API
- Adjusts for ambient noise automatically
- Handles timeout and error cases gracefully

### Text-to-Speech
- Configurable voice settings
- Attempts to use male voice for JARVIS-like experience
- Adjustable speech rate and volume

### GUI Interface
- Dark theme inspired by Iron Man's interface
- Real-time chat display
- Voice listening toggle
- Text input option
- Status indicators

### AI Intelligence
- **Conversation Memory**: Remembers past interactions and context
- **Learning Capabilities**: Adapts responses based on user patterns
- **Sentiment Analysis**: Responds appropriately to user emotions
- **Personalized Responses**: Uses "captain" and learns user preferences
- **Smart Suggestions**: Provides contextual recommendations
- **Usage Pattern Recognition**: Learns from command frequency and timing

## Customization

### Adding New Commands
Edit the `process_command` method in `main.py` to add new voice commands:

```python
elif 'your command' in command:
    # Your custom logic here
    response = "Your response"
    self.speak(response)
    self.brain.add_to_memory(original_command, response, self.conversation_context)
```

### Voice Settings
Modify the `setup_voice` method to change voice characteristics:

```python
self.tts_engine.setProperty('rate', 180)    # Speech speed
self.tts_engine.setProperty('volume', 0.9)  # Volume level
```

### GUI Appearance
Customize colors and fonts in the `setup_styles` method of `gui.py`.

## Requirements

- Python 3.7+
- Microphone access
- Internet connection (for speech recognition and web searches)
- Windows OS (some features are Windows-specific)
- Storage space for AI learning data (creates `jarvis_data/` folder)

## Troubleshooting

### Microphone Issues
- Ensure your microphone is properly connected
- Check Windows privacy settings for microphone access
- Try running as administrator if permission issues occur

### Speech Recognition Issues
- Requires internet connection for Google Speech Recognition
- Speak clearly and at moderate pace
- Reduce background noise

### PyAudio Installation Issues
- Download the appropriate wheel file for your Python version
- Use: `pip install path/to/downloaded/wheel.whl`

## AI Features

### Learning Capabilities
- **Conversation Memory**: Stores up to 100 recent interactions
- **Pattern Recognition**: Learns from command usage patterns
- **Preference Storage**: Remembers user preferences and information
- **Context Awareness**: Maintains conversation context across sessions
- **Sentiment Analysis**: Adapts responses based on detected emotions

### Data Storage
L.U.F.F.Y creates a `jarvis_data/` folder to store:
- `preferences.json` - User preferences and settings
- `user_profile.json` - Usage patterns and statistics
- `patterns.pkl` - Learned command patterns
- `tasks.json` - Task automation and reminders

## Future Enhancements

- Weather API integration with location learning
- Smart home device control with usage patterns
- Email and calendar management with AI scheduling
- Advanced conversation AI with personality development
- Custom wake word detection
- Multi-language support with preference learning

## License

This project is for educational and personal use. L.U.F.F.Y represents an evolution in personal AI assistants with learning capabilities.

---

**"The best AI is one that grows with you."** - L.U.F.F.Y Philosophy
