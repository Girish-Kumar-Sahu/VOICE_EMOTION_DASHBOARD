# 🎙️ AI Voice Analyzer Dashboard (Development Version)

An AI-powered Voice Analyzer Dashboard built using **Python**, **Flask**, and modern AI tools.  
This project allows users to upload `.wav` audio files, converts speech to text, performs sentiment analysis, and visualizes emotional trends on a simple dashboard.

⚠️ This repository contains the **local development version** of the project. Deployment is currently in progress as part of my learning journey.

---

## 🚀 Features

- Upload and analyze `.wav` voice recordings
- Speech-to-text conversion
- AI-based sentiment analysis
- Emotion timeline visualization with charts
- Simple monitoring-style dashboard UI

---

## 🧠 Tech Stack

- Python
- Flask
- SpeechRecognition
- HTML / CSS / Chart.js
- Requests API

---

## 📂 Project Structure

voice-emotion-dashboard/
│
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
└── README.md

yaml
Copy code

---

## ⚙️ Installation (Local Development)

### 1️⃣ Clone the repository


git clone https://github.com/YOUR-USERNAME/voice-emotion-dashboard.git
cd voice-emotion-dashboard
2️⃣ Create virtual environment (recommended)
bash
Copy code
python -m venv venv
Activate it:

Windows

bash
Copy code
venv\Scripts\activate
Mac/Linux

Copy code
source venv/bin/activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the application
bash
Copy code
python app.py
Open in browser:

cpp
Copy code
http://127.0.0.1:5000
🎧 Usage
Upload a .wav audio file.

The app converts speech into text.

Sentiment analysis runs on the extracted text.

The dashboard displays detected emotion and timeline chart.

⚠️ Important Notes
Only .wav files are supported in the current development version.

This project is still under active learning and improvement.

Deployment setup is being explored (Render / cloud deployment).
