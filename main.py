import base64
import io
import json
import os
import time
import wave

import pyaudio
import requests
import speech_recognition as sr


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        text = r.recognize_google(audio, language="ja-JP")
        return text


def voicevox_speak(text, speaker):
    params = {
        "text": text,
        "speaker": speaker,
    }
    audio_query = requests.post(
        "http://127.0.0.1:50021/audio_query",
        params=params
    )
    audio_query_json = json.dumps(audio_query.json())
    synthesized = requests.post(
        "http://127.0.0.1:50021/synthesis",
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
    time.sleep(0.1)
    stream.stop_stream
    stream.close()
    p.terminate()


def coeiroink_speak(text, speaker):
    params = {
        "text": text,
        "speaker": speaker,
    }
    audio_query = requests.post(
        "http://127.0.0.1:50031/audio_query",
        params=params
    )
    audio_query_json = json.dumps(audio_query.json())
    synthesized = requests.post(
        "http://127.0.0.1:50031/synthesis",
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
    time.sleep(0.1)
    stream.stop_stream
    stream.close()
    p.terminate()


def sharevox_speak(text, speaker):
    params = {
        "text": text,
        "speaker": speaker,
    }
    audio_query = requests.post(
        "http://127.0.0.1:50025/audio_query",
        params=params
    )
    audio_query_json = json.dumps(audio_query.json())
    synthesized = requests.post(
        "http://127.0.0.1:50025/synthesis",
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
    time.sleep(0.1)
    stream.stop_stream
    stream.close()
    p.terminate()


def capcut_speak(text, speaker):
    data = {
        "text": text,
        "speaker": speaker,
    }

    synthesized = requests.post(
        "https://api.vxxx.cf/tts/synthesize",
        json=data
    ).json()

    audio = io.BytesIO(base64.b64decode(synthesized["content"]))
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
    time.sleep(0.1)
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
    response = requests.post(
        "https://api-mebo.dev/api",
        data=data_encoded,
        headers={"Content-Type": "application/json"},
    ).json()
    ai_response = response["bestResponse"]["utterance"]
    print(ai_response)
    return ai_response
