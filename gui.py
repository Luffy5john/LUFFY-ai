"""
L.U.F.F.Y GUI - Graphical User Interface for the AI Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import time
from main import LUFFY

class LUFFYGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("L.U.F.F.Y - AI Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize L.U.F.F.Y
        self.luffy = LUFFY()
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        self.setup_gui()
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
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
        self.status_label = ttk.Label(self.root, text="● OFFLINE", style='Status.TLabel')
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
        self.listening = False
        self.add_to_chat("L.U.F.F.Y", "System initialized. Ready for commands.")
        self.update_status("ONLINE")
        
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
        
    def update_status(self, status):
        """Update status indicator"""
        if status == "ONLINE":
            self.status_label.config(text="● ONLINE", foreground='#00ff00')
        elif status == "LISTENING":
            self.status_label.config(text="● LISTENING", foreground='#ffff00')
        elif status == "PROCESSING":
            self.status_label.config(text="● PROCESSING", foreground='#ff8800')
        else:
            self.status_label.config(text="● OFFLINE", foreground='#ff0000')
    
    def send_command(self, event=None):
        """Send text command"""
        command = self.command_entry.get().strip()
        if command:
            self.add_to_chat("You", command)
            self.command_entry.delete(0, tk.END)
            
            # Process command in separate thread
            threading.Thread(target=self.process_command_thread, args=(command,), daemon=True).start()
    
    def process_command_thread(self, command):
        """Process command in separate thread"""
        self.update_status("PROCESSING")
        
        # Capture L.U.F.F.Y response
        original_speak = self.luffy.speak
        response_text = ""
        
        def capture_speak(text):
            nonlocal response_text
            response_text = text
            original_speak(text)
        
        self.luffy.speak = capture_speak
        self.luffy.process_command(command)
        self.luffy.speak = original_speak
        
        if response_text:
            self.root.after(0, lambda: self.add_to_chat("L.U.F.F.Y", response_text))
        
        self.root.after(0, lambda: self.update_status("ONLINE"))
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not self.listening:
            self.listening = True
            self.listen_button.config(text="🛑 Stop")
            self.update_status("LISTENING")
            threading.Thread(target=self.listen_thread, daemon=True).start()
        else:
            self.listening = False
            self.listen_button.config(text="🎤 Listen")
            self.update_status("ONLINE")
    
    def listen_thread(self):
        """Voice listening thread"""
        while self.listening:
            try:
                command = self.luffy.listen()
                if command and self.listening:
                    self.root.after(0, lambda cmd=command: self.add_to_chat("You", cmd))
                    self.root.after(0, lambda cmd=command: threading.Thread(
                        target=self.process_command_thread, args=(cmd,), daemon=True).start())
            except Exception as e:
                print(f"Listening error: {e}")
                break
        
        self.root.after(0, lambda: self.update_status("ONLINE"))
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_to_chat("L.U.F.F.Y", "Chat cleared. How may I assist you?")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LUFFYGui()
    app.run()
