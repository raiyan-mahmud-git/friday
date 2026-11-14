# Friday AI Assistant

Friday is a Python voice assistant for your desktop, with a browser demo for trying its AI conversation. The desktop app listens for a wake word, speaks replies, manages timers and reminders, opens websites, and can play songs from your library. The browser demo lets visitors chat with Friday without installing Python.

## Try the browser demo

The demo runs on [Streamlit Community Cloud](https://streamlit.io/cloud). To publish it after renaming the GitHub repository:

1. Sign in to Streamlit Community Cloud with GitHub and deploy this repository.
2. Set **Main file path** to `web_demo.py`.
3. In **Advanced settings**, choose Python **3.12**.
4. In the app's **Secrets** settings, add:

   ```toml
   GROQ_API_KEY = "your-groq-key"
   AI_MODEL = "openai/gpt-oss-20b"
   ```

5. Share the Streamlit app URL. The API key stays in the app's server-side secrets and is not sent to visitors.

The web demo provides AI chat only. It cannot use a visitor's microphone, speakers, or desktop controls. The voice assistant is run locally.

## Run the desktop voice assistant

### Requirements

- Python 3.10 or newer
- A working microphone and speakers
- Internet access for speech recognition, speech synthesis, and AI replies
- A [Groq API key](https://console.groq.com/keys)
- A [NewsAPI key](https://newsapi.org) (optional)

### Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-desktop.txt
Copy-Item .env.example .env
```

Edit `.env` and add your keys. On macOS/Linux, activate the environment with `source .venv/bin/activate`. PyAudio may need PortAudio installed first on macOS/Linux; on Windows, use a compatible PyAudio wheel if installation fails.

Start the desktop assistant:

```sh
python main.py
```

Check the AI connection separately with `python client.py`.

## Voice commands

Say **“Friday”**, wait for “Yes sir?”, then give a command.

| Say | What happens |
|---|---|
| “open YouTube” | Opens YouTube in your browser |
| “play faded” | Opens that song from `musicLibrary.py` |
| “tell me the news” | Reads up to five US headlines (requires NewsAPI key) |
| “set a timer for 5 minutes” | Starts a timer |
| “remind me to stretch in 10 minutes” | Sets a reminder |
| “how much time is left on my timer” | Lists active timers and reminders |
| “cancel all timers” | Cancels active timers and reminders |
| “what is the capital of France” | Sends the question to the AI |
| “goodbye” | Shuts Friday down |

Press `Ctrl+C` in the terminal to stop the assistant.

## Configuration

Copy `.env.example` to `.env` for local use. For Streamlit hosting, configure the secrets in the app settings instead.

| Variable | Default | Purpose |
|---|---|---|
| `GROQ_API_KEY` | — | Required for AI answers and the web demo |
| `NEWS_API_KEY` | — | Optional news headlines key |
| `AI_MODEL` | `openai/gpt-oss-20b` | Model used for AI replies |
| `FRIDAY_VOICE` | `en-GB-RyanNeural` | Desktop text-to-speech voice |
| `WAKE_WORD` | `friday` | Desktop wake word |

For compatibility, the desktop app still accepts the old `JARVIS_VOICE` setting if `FRIDAY_VOICE` is not set.

To add songs, edit `musicLibrary.py` and add an entry like `"song name": "https://youtube.com/watch?v=..."`.

## Project files

- `main.py` — desktop wake-word loop, voice, commands, and AI replies
- `web_demo.py` — hosted browser chat demo
- `timers.py` — timer and reminder logic
- `musicLibrary.py` — song names and links
- `client.py` — quick Groq API connection check
- `requirements.txt` — web demo dependencies for Streamlit Community Cloud
- `requirements-desktop.txt` — desktop voice assistant dependencies
- `.env.example` — local configuration template (no real credentials)
