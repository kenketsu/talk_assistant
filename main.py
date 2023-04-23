import io
import json
import os
import wave

import keyboard
import pyaudio
import requests
import speech_recognition as sr
from dotenv import load_dotenv

r = sr.Recognizer()

load_dotenv(".env")


def listen():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ja-JP")
            return text
        except Exception:
            print("音声を認識できませんでした。")


def alt_listen():
    recognized_text = None
    while True:
        if keyboard.is_pressed("alt"):
            recognized_text = listen()
        elif not keyboard.is_pressed("alt"):
            if recognized_text is None:
                continue
            else:
                print(recognized_text)
                return recognized_text


def speak(text, speaker):
    params = {
        "text": text,
        "speaker": speaker,
    }
    audio_query = requests.post(
        "http://localhost:50021/audio_query",
        params=params
    )
    audio_query_json = json.dumps(audio_query.json())
    synthesized = requests.post(
        "http://localhost:50021/synthesis",
        data=audio_query_json,
        params={"speaker": speaker},
        headers={"Content-Type": "application/json"},
    )

    audio = io.BytesIO(synthesized.content)
    wf = wave.open(audio, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    )

    chunk = 1024
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream
    stream.close()
    p.terminate()


def get_ai_response(recognized_text):
    data = {
        "api_key": os.getenv("MIIBO_API_KEY"),
        "agent_id": os.getenv("MIIBO_AGENT_ID"),
        "utterance": recognized_text,
    }
    data_encoded = json.dumps(data)
    ai_response = requests.post(
        "https://api-mebo.dev/api",
        data=data_encoded,
        headers={"Content-Type": "application/json"},
    )
    return ai_response


class TalkFriends():
    def __init__(self) -> None:
        self.is_active = False

    def deactivate(self):
        self.is_active = False

    def main(self):
        self.is_active = True
        while self.is_active:
            text = alt_listen()
            speak(text, 43)


t = TalkFriends()
t.main()
