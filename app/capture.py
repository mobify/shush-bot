import pyaudio

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# On my system, device 2 is a USB microphone, your number may differ.
INPUT_STREAM = pyaud.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input_device_index=None,
    input=True
)
