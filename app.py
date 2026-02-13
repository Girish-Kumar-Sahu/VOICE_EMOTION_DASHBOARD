from flask import Flask, render_template, request
import speech_recognition as sr
import os
import requests
from datetime import datetime

app = Flask(__name__)

emotion_history = []

@app.route("/health")
def health():
    return "OK"

@app.route("/")
def home():
    return render_template("index.html", history=emotion_history)

def analyze_sentiment(text):
    url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
    response = requests.post(url, json={"inputs": text})

    try:
        data = response.json()

        # HF returns nested list
        if isinstance(data, list) and len(data) > 0:
            top = max(data[0], key=lambda x: x["score"])
            label = top["label"]
            score = round(top["score"], 2)

            # 🔥 Convert LABEL_* to POSITIVE/NEGATIVE
            if label == "LABEL_2":
                return "POSITIVE", score
            elif label == "LABEL_0":
                return "NEGATIVE", score
            else:
                return "NEUTRAL", score

    except Exception as e:
        print("Sentiment error:", e)

    return "LOADING", 0



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

    emotion, score = analyze_sentiment(text)

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
