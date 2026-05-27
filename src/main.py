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
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai library not found. Please install 'google-genai'.")
    sys.exit(1)

from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env file")

MODELS = [
    {"id": "gemini-2.5-flash-lite", "label": "2.5 Flash Lite (20/d)"},
    {"id": "gemini-3.1-flash-lite", "label": "3.1 Flash Lite (500/d)"},
    {"id": "gemini-2.5-flash",      "label": "2.5 Flash (20/d)"},
    {"id": "gemini-3-flash",        "label": "3 Flash (20/d)"},
    {"id": "gemini-3.5-flash",      "label": "3.5 Flash BEST (20/d)"},
    {"id": "gemma-4-31b-it",        "label": "Gemma 4 31B (1500/d)"},
]
DEFAULT_MODEL_INDEX = 1

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
        self.model_index = DEFAULT_MODEL_INDEX
        self._revert_after_id = None

        self.client = None
        self.setup_ai()
        self.setup_overlay()
        self.setup_hotkeys()
        log(f"Model: {self.current_model()['label']}")
        log("Initialization complete.")

    def current_model(self):
        return MODELS[self.model_index]

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
            self.client = genai.Client(api_key=API_KEY)
            log("AI Client configured (Google AI Studio).")
        except Exception as e:
            log(f"Error configuring AI: {e}")
            self.response_text.set("AI Config Error")

    def process_screenshot(self):
        """Captures screen, sends to Gemini, updates overlay."""
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

            model = self.current_model()
            log(f"Sending request to Gemini ({model['id']})...")

            response = self.client.models.generate_content(
                model=model["id"],
                contents=[
                    SYSTEM_PROMPT + "\nFind the question and provide the answer.",
                    screenshot,
                ],
                config=types.GenerateContentConfig(temperature=0.1),
            )

            answer = (response.text or "").strip()
            if answer:
                log(f"Response received ({time.time() - start_time:.2f}s): {answer}")
                self.response_text.set(answer)
            else:
                log("No text in response.")
                self.response_text.set("No response")

            if not self.is_visible:
                self.root.after(0, self.show_overlay)

        except Exception as e:
            log(f"Error processing: {e}")
            self.response_text.set(f"Error: {str(e)[:40]}")
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

    def cycle_model(self):
        """Handler for ']' key. Cycles to the next model and shows its name briefly."""
        if self.processing:
            log("Ignored ']' - request in progress.")
            return
        self.model_index = (self.model_index + 1) % len(MODELS)
        model = self.current_model()
        log(f"Model -> {model['id']}")
        self.flash_status(f">> {model['label']}")

    def flash_status(self, text, duration_ms=1800):
        """Show a transient status in the overlay, then revert to 'Ready'."""
        if not self.is_visible:
            self.root.after(0, self.show_overlay)
        self.response_text.set(text)
        if self._revert_after_id is not None:
            try:
                self.root.after_cancel(self._revert_after_id)
            except Exception:
                pass
        self._revert_after_id = self.root.after(duration_ms, self._revert_status)

    def _revert_status(self):
        self._revert_after_id = None
        if not self.processing:
            self.response_text.set("Ready")

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
            keyboard.add_hotkey(']', self.cycle_model)
            log("Hotkeys: '/' scan, '.' toggle, '-' move, ']' model, '=' quit.")
        except Exception as e:
            log(f"Hotkey Error: {e}")
            self.response_text.set("Hotkey Error (Run as Admin?)")

    def run(self):
        log("Application loop starting...")
        print("Press '=' to quit application safe.")
        self.root.mainloop()

if __name__ == "__main__":
    if not API_KEY:
        print("Set GEMINI_API_KEY in .env file first!")
    else:
        app = StealthAgent()
        app.run()
