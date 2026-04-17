from openai import OpenAI
import base64

client = OpenAI()

# -----------------------------
# 1. SPEECH → TEXT
# -----------------------------
def speech_to_text(audio_binary):
    """
    Convert audio bytes to text using OpenAI Whisper.
    """
    try:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=("audio.wav", audio_binary)
        )
        return response.text
    except Exception as e:
        print("STT Error:", e)
        return "Error converting speech to text."


# -----------------------------
# 2. TEXT → SPEECH
# -----------------------------
def text_to_speech(text, voice="alloy"):
    """
    Convert text to spoken audio using OpenAI TTS.
    Returns raw audio bytes.
    """
    try:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        return response.read()  # raw audio bytes
    except Exception as e:
        print("TTS Error:", e)
        return None


# -----------------------------
# 3. PROCESS USER MESSAGE (CHATGPT)
# -----------------------------
def openai_process_message(user_message):
    """
    Send user text to OpenAI GPT model and return the response text.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("ChatGPT Error:", e)
        return "Sorry, I could not process that."
