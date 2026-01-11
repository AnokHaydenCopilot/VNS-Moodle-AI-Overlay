import os
import sys
import threading
import time
import datetime
import io
try:
    import tkinter as tk
except ImportError:
    print("CRITICAL ERROR: 'tkinter' library is missing.")
    sys.exit(1)

try:
    import keyboard
except ImportError:
    print("Keyboard library not found. Please install it.")
    sys.exit(1)

try:
    from groq import Groq
except ImportError:
    print("Groq library not found. Please install 'groq'.")
    sys.exit(1)

import base64
from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("Warning: GROQ_API_KEY not found in .env file")

MODEL_NAME = "meta-llama/llama-4-maverick-17b-128e-instruct"

SYSTEM_PROMPT = """You are a precise exam assistant. You will see a screenshot of a test question.
Your task: Identify the correct answer immediately.
Constraints:
1. Output ONLY the answer text or the letter (e.g., "True", "b, c", "Economy").
2. No explanations. No filler words.
3. If it's a fill-in-the-blank, provide just the word.
4. Keep it extremely short suitable for a small overlay.
If you cannot see a question, output "No question found"."""

def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

class StealthAgent:
    def __init__(self):
        log("Initializing Stealth Agent...")
        self.root = tk.Tk()
        self.response_text = tk.StringVar(value="Ready")
        self.is_visible = True
        self.processing = False
        self.is_draggable = False
        
        self.client = None
        self.setup_ai()
        self.setup_overlay()
        self.setup_hotkeys()
        log("Initialization complete.")

    def setup_overlay(self):
        self.root.overrideredirect(True)  
        self.root.attributes("-topmost", True)  
        
        self.bg_color = "black" 
        self.text_color = "#FFFFFF" 
        
        self.root.config(bg=self.bg_color)
        
        try:
            self.root.attributes("-transparentcolor", self.bg_color)
            self.root.attributes("-alpha", 0.5) 
        except tk.TclError:
            pass
        
        self.label = tk.Label(
            self.root, 
            textvariable=self.response_text,
            font=("Consolas", 12, "bold"), 
            fg=self.text_color,
            bg=self.bg_color,
            wraplength=400,
            justify="left"
        )
        self.label.pack(anchor="w", padx=10, pady=5)

        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if screen_width == 0: screen_width = 1920
        if screen_height == 0: screen_height = 1080
        
        self.root.geometry(f"450x120+50+{screen_height - 180}")

    def start_move(self, event):
        if not self.is_draggable: return
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        if not self.is_draggable: return
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def setup_ai(self):
        try:
            self.client = Groq(api_key=API_KEY)
            log("AI Client configured (Groq).")
        except Exception as e:
            log(f"Error configuring AI: {e}")
            self.response_text.set("AI Config Error")

    def encode_image(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def process_screenshot(self):
        """Captures screen, sends to Groq/LLaMA, updates overlay."""
        if self.processing:
            log("Ignored '/' - already processing.")
            return
            
        self.processing = True
        self.response_text.set("Analyzing...")
        self.root.after(0, self.root.update) 
        
        start_time = time.time()
        try:
            log("Taking screenshot...")
            screenshot = ImageGrab.grab()
            
            base64_image = self.encode_image(screenshot)
            
            log(f"Sending request to Groq ({MODEL_NAME})...")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": SYSTEM_PROMPT + "\nFind the question and provide the answer."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                model=MODEL_NAME,
                temperature=0.1,
            )
            
            answer = chat_completion.choices[0].message.content
            if answer:
                answer = answer.strip()
                log(f"Response received ({time.time() - start_time:.2f}s): {answer}")
                self.response_text.set(answer)
            else:
                log("No text in response.")
                self.response_text.set("No response")
                
            if not self.is_visible:
                self.root.after(0, self.show_overlay)
                
        except Exception as e:
            log(f"Error processing: {e}")
            self.response_text.set(f"Error: {str(e)[:20]}...")
        finally:
            self.processing = False


    def on_slash_press(self):
        """Handler for '/' key."""
        log("Key '/' pressed.")
        threading.Thread(target=self.process_screenshot, daemon=True).start()

    def show_overlay(self):
        log("Showing overlay.")
        self.root.deiconify()
        self.is_visible = True

    def toggle_visibility(self, e=None):
        """Handler for '.' key."""
        log("Key '.' pressed.")
        if self.is_visible:
            self.root.withdraw() 
            self.is_visible = False
            log("Overlay hidden.")
        else:
            self.root.deiconify() 
            self.is_visible = True
            log("Overlay shown.")

    def toggle_dragging(self):
        """Handler for '-' key."""
        self.is_draggable = not self.is_draggable
        state = "enabled" if self.is_draggable else "disabled"
        log(f"Dragging {state}.")
        if self.is_draggable:
            self.root.config(cursor="fleur")
            self.label.config(cursor="fleur")
        else:
            self.root.config(cursor="arrow")
            self.label.config(cursor="arrow")

    def quit_app(self):
        """Handler for '=' key to quit."""
        log("Quitting application...")
        self.root.quit()
        sys.exit(0)

    def setup_hotkeys(self):
        try:
            keyboard.add_hotkey('/', self.on_slash_press)
            keyboard.add_hotkey('.', self.toggle_visibility)
            keyboard.add_hotkey('-', self.toggle_dragging)
            keyboard.add_hotkey('=', self.quit_app)
            log("Hotkeys registered: '/' to capture, '.' to toggle, '-' to move, '=' to quit.")
        except Exception as e:
            log(f"Hotkey Error: {e}")
            self.response_text.set("Hotkey Error (Run as Admin?)")

    def run(self):
        log("Application loop starting...")
        print("Press '=' to quit application safely.")
        self.root.mainloop()

if __name__ == "__main__":
    if not API_KEY:
        print("Set GROQ_API_KEY in .env file first!")
    else:
        app = StealthAgent()
        app.run()
