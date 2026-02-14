from flask import Flask, render_template, request
import speech_recognition as sr
from transformers import pipeline
import os
from datetime import datetime

app = Flask(__name__)

# Load model once
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# 🔥 Emotion history storage
emotion_history = []

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

    result = sentiment_analyzer(text)[0]

    os.remove(filepath)

    # 🕒 Capture current minute & second
    current_time = datetime.now().strftime("%M:%S")

    # Convert emotion to numeric value for chart
    emotion_value = 1 if result['label'] == "POSITIVE" else -1

    # Save to history
    emotion_history.append({
        "time": current_time,
        "emotion": result['label'],
        "score": round(result['score'], 2),
        "value": emotion_value
    })

    return render_template(
        "index.html",
        text=text,
        emotion=result['label'],
        score=round(result['score'], 2),
        history=emotion_history
    )

if __name__ == "__main__":
    app.run(debug=True)
