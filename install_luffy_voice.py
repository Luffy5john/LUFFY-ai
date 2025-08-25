#!/usr/bin/env python3
"""
L.U.F.F.Y Voice Enhancement Script
Installs advanced voice synthesis for Luffy character
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False

def main():
    print("Installing Luffy Voice Enhancement for L.U.F.F.Y...")
    
    # Advanced TTS packages for better voice quality
    packages = [
        "edge-tts",  # Microsoft Edge TTS with more natural voices
        "gTTS",      # Google Text-to-Speech
        "pygame",    # For audio playback
        "pydub",     # Audio processing
    ]
    
    print("\nInstalling voice enhancement packages...")
    for package in packages:
        install_package(package)
    
    print("\nVoice packages installed!")
    print("\nNext steps:")
    print("1. Run the enhanced L.U.F.F.Y system")
    print("2. L.U.F.F.Y will now have more natural, energetic voice")
    print("3. Voice will match Luffy's personality better!")
    
    print("\nReady to set sail with enhanced Luffy voice!")

if __name__ == "__main__":
    main()
