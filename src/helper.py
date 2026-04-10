import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def voice_input():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # ✅ improve accuracy
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
        return ""   # ✅ IMPORTANT: return empty string

    except sr.RequestError as e:
        print(f"API error: {e}")
        return ""   # ✅ IMPORTANT


def text_to_speech(text):
    if not text or text.strip() == "":
        return  # ✅ avoid empty TTS

    tts = gTTS(text=text, lang="en")
    tts.save("speech.mp3")


def llm_model_object(user_text):
    # ✅ FIX: empty input check
    if not user_text or user_text.strip() == "":
        return "Please say something."

    model = genai.GenerativeModel('gemini-pro')

    try:
        response = model.generate_content(user_text)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"