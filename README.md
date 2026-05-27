# VNS/ВНС/Moodle AI overlay 👻

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**VNS/ВНС/Moodle AI overlay** is a lightweight, stealthy AI-powered screen overlay for real-time visual analysis. Designed to be unobtrusive, it helps users quickly analyze screen content using advanced Vision AI models via Groq.

## Demonstration
[▶ Watch video](https://github.com/user-attachments/assets/ab014efa-9cf0-4bd6-94ac-d9ad6d0412e2)

**Windows support**

## Features

- **Stealth Mode:** Semi-transparent, draggable overlay that blends into your desktop.
- **Instant Analysis:** Captures screen content and uses Llama-based Vision models to provide immediate answers.
- **Minimalist Interface:** Shows only what you need, when you need it.
- **Keyboard Control:** Controlled entirely via global hotkeys for speed and discretion.
- **Drag & Lock:** Position the overlay anywhere on your screen and lock it in place.

## Installation

1.  **Clone the repository**

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    # Or manually create .env and add your key
    ```

2.  Open `.env` and add your Groq API Key:
    ```ini
    GEMINI_API_KEY=your_api_key_here
    ```
    *Get your free API key at [Google AI Studio](https://aistudio.google.com/apikey).*

## Usage

Run the script or start via Python:

```bash
python src/main.py
```

### Hotkeys

| Key | Action |
| :--- | :--- |
| **`/`** | **Scan Screen:** Captures the current screen and asks the AI for an answer. |
| **`.`** | **Toggle Visibility:** Hides or shows the overlay instantly. |
| **`-`** | **Move/Lock:** Toggles "Drag Mode". When enabled, click and drag the text. |
| **`]`** | **Cycle Model:** Switches to the next vision model in the list. |
| **`=`** | **Quit:** Safely closes the application. |


### Available Models (Free API) (cycled via `]`)

Free-tier limits on Google AI Studio:

| # | Model ID | RPD |
| :--- | :--- | :--- |
| 1 | `gemini-2.5-flash-lite` | 20 |
| 2 | `gemini-3.1-flash-lite` *(default)* | 500 |
| 3 | `gemini-2.5-flash` | 20 |
| 4 | `gemini-3-flash` | 20 |
| 5 | `gemini-3.5-flash` *(strongest)* | 20 |
| 6 | `gemma-4-31b-it` | 1500 |

## ⚠️ Legal & Ethical Disclaimer

**EDUCATIONAL PURPOSES ONLY.**

This tool is designed for educational experimentation with Computer Vision and Large Language Models. The author uses this software for testing latency and accuracy of open-source models in real-time environments.

**The author is not responsible for any misuse of this tool.** Using this software to gain an unfair advantage in academic evaluations, cheat on tests, or violate the Terms of Service of educational platforms is strictly prohibited and unethical. Users assume full responsibility for complying with all applicable laws and institutional regulations.
