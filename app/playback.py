import pyaudio
import wave
import os
import random

shushing = False
samples_path = "app/sound-samples"

def get_random_shush():
    # Need to check if the item is a file.
    return os.path.join(samples_path, random.choice(os.listdir(samples_path)))

def shush():
    shushing = True
    chunk = 1024
    wf = wave.open(get_random_shush(), "rb")
    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
    shushing = False
