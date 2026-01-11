# VNS/ВНС/Moodle AI overlay 👻

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**VNS/ВНС/Moodle AI overlay** is a lightweight, stealthy AI-powered screen overlay for real-time visual analysis. Designed to be unobtrusive, it helps users quickly analyze screen content using advanced Vision AI models via Groq.

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
    GROQ_API_KEY=gsk_your_api_key_here
    ```
    *Get your free API key at [Groq Console](https://console.groq.com/keys).*

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
| **`=`** | **Quit:** Safely closes the application. |

## ⚠️ Legal & Ethical Disclaimer

**EDUCATIONAL PURPOSES ONLY.**

This tool is designed for educational experimentation with Computer Vision and Large Language Models. The author uses this software for testing latency and accuracy of open-source models in real-time environments.

**The author is not responsible for any misuse of this tool.** Using this software to gain an unfair advantage in academic evaluations, cheat on tests, or violate the Terms of Service of educational platforms is strictly prohibited and unethical. Users assume full responsibility for complying with all applicable laws and institutional regulations.
