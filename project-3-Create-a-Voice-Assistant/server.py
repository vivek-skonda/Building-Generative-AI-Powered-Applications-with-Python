import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from worker import speech_to_text, text_to_speech, openai_process_message

app = Flask(__name__)
CORS(app)


# -----------------------------
# 1. FRONTEND PAGE
# -----------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# -----------------------------
# 2. SPEECH → TEXT API
# -----------------------------
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return jsonify({"text": text})


# -----------------------------
# 3. PROCESS MESSAGE (CHATGPT)
# -----------------------------
@app.route('/process-message', methods=['POST'])
def process_message_route():
    data = request.get_json()
    user_message = data.get("message", "")
    response_text = openai_process_message(user_message)
    return jsonify({"response": response_text})


# -----------------------------
# 4. TEXT → SPEECH API
# -----------------------------
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech_route():
    data = request.get_json()
    text = data.get("text", "")
    voice = data.get("voice", "alloy")

    audio_bytes = text_to_speech(text, voice)

    if audio_bytes is None:
        return jsonify({"error": "TTS failed"}), 500

    # Encode audio to base64 for frontend
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return jsonify({"audio": audio_base64})


# -----------------------------
# 5. RUN SERVER
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
