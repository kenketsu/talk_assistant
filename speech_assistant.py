import base64
import io
import json
import os

import requests
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

# 音声をテキストに変換
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        text = r.recognize_google(audio, language="ja-JP")
        return text


# koeiro apiで再生
def koeiro_speak(text, speaker_x, speaker_y, style):
    data = {
        "text": text,
        "speaker_x": speaker_x,
        "speaker_y": speaker_y,
        "style": style,
    }
    synthesized = requests.post(
        "https://api.rinna.co.jp/models/cttse/koeiro",
        json=data,
        headers={"Content-Type": "application/json"}
    ).json()
    formatted = synthesized["audio"][24:]
    audio = io.BytesIO(base64.b64decode(formatted))
    data, samplerate = sf.read(audio)
    sd.play(data, samplerate)
    sd.wait()


# miiboから返答を取得
def get_ai_response(recognized_text):
    data = {
        "api_key": os.getenv("MIIBO_API_KEY"),
        "agent_id": os.getenv("MIIBO_AGENT_ID"),
        "utterance": recognized_text,
    }
    data_encoded = json.dumps(data)
    response = requests.post(
        "https://api-mebo.dev/api",
        data=data_encoded,
        headers={"Content-Type": "application/json"},
    ).json()
    ai_response = response["bestResponse"]["utterance"]
    return ai_response
