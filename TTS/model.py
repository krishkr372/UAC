import pyttsx3
import threading

def speak(text):
    # speak the provided text in an isolated background thread
    if not text.strip():
        return  # Do not speak empty or whitespace-only text

    def target():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    thread = threading.Thread(target=target, daemon=True).start()
    