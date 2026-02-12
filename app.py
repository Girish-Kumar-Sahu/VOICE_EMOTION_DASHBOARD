from flask import Flask, render_template, request
import speech_recognition as sr
import os
import requests
import time
from datetime import datetime

app = Flask(__name__)

# HuggingFace API setup
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/health")
def health():
    return "OK"

# Emotion history storage
emotion_history = []

# 🔥 SAFE HF QUERY FUNCTION
def query_huggingface(text):
    payload = {"inputs": text}
    max_retries = 5

    for attempt in range(max_retries):
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        try:
            result = response.json()
        except:
            print("HF RAW RESPONSE:", response.text)
            return {"error": "Invalid API response"}

        # ✅ Correct prediction format
        if isinstance(result, list) and len(result) > 0:
            return result

        # 🔁 Model loading handling
        elif isinstance(result, dict) and "error" in result:
            if "loading" in result["error"].lower() or "model" in result["error"].lower():
                print(f"Model loading... retry {attempt+1}")
                time.sleep(8)
                continue
            else:
                return result

        else:
            return result

    return {"error": "Model failed to load"}

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

    # 🔥 Call HF API
    response = query_huggingface(text)
    print("HF RESPONSE:", response)

    # ✅ FIXED PARSING (IMPORTANT CHANGE)
    if isinstance(response, list) and len(response) > 0:
        api_result = response[0]
        emotion = api_result.get("label", "ERROR")
        score = round(api_result.get("score", 0), 2)
    else:
        emotion = "LOADING"
        score = 0

    if os.path.exists(filepath):
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
