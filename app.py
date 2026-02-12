from flask import Flask, render_template, request
import speech_recognition as sr
import os
import requests
from datetime import datetime

app = Flask(__name__)

# HuggingFace API setup
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route("/health")
def health():
    return "OK"

# Emotion history storage
emotion_history = []

def query_huggingface(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    return render_template("index.html", history=emotion_history)

@app.route("/analyze", methods=["POST"])
def analyze():
    audio_file = request.files["audio"]

    filepath = "temp_audio.wav"
    audio_file.save(filepath)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    except:
        text = "Could not understand audio"

    # 🔥 Call HuggingFace API
    
    response = query_huggingface(text)
    print("HF RESPONSE:", response)

    # Handle API loading or error responses safely
    if isinstance(response, dict):
        emotion = "LOADING"
        score = 0
    else:
        api_result = response[0][0]
        emotion = api_result["label"]
        score = round(api_result["score"], 2)

    os.remove(filepath)

    current_time = datetime.now().strftime("%M:%S")
    
    if emotion in ["POSITIVE", "NEGATIVE"]:
        emotion_value = 1 if emotion == "POSITIVE" else -1

        emotion_history.append({
            "time": current_time,
            "emotion": emotion,
            "score": score,
            "value": emotion_value
        })

    return render_template(
        "index.html",
        text=text,
        emotion=emotion,
        score=score,
        history=emotion_history
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
