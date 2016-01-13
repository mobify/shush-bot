import numpy
import pyaudio
import analyse
import wave
import time

shushing = False
loudness = -40

def shush():
    shushing = True
    chunk = 1024
    wf = wave.open('app/sound-samples/shush.wav', 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    data = wf.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
    shushing = False

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 2 is a USB microphone, your number may differ.
stream = pyaud.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input_device_index=None,
    input=True
)

while True:

    if not shushing:

        # Read raw microphone data
        rawsamps = stream.read(1024, exception_on_overflow=False)

        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)

        loudness = analyse.loudness(samps)

        # Show the volume and pitch
        print loudness

    if loudness > -7:
        stream.stop_stream()
        shush()
        stream.start_stream()
