import numpy
import analyse
import signal
import sys

from capture import INPUT_STREAM
from playback import shush
from visualize import show_loudness
from web_client import update_config
from web_client import local_state
from threading import Timer

# App Constants
SHUSHBOT_ID = 1

def signal_handler(signal, frame):
    print('Goodbye!')
    sys.exit(0)

def main():

    # Initial values.
    signal.signal(signal.SIGINT, signal_handler)

    # Kickoff the auto updating config
    Timer(0, update_config, [SHUSHBOT_ID]).start()

    threshold, volume = (
        local_state["threshold"],
        local_state["volume"]
    )

    # Main control loop.
    while True:
        # Read raw microphone data
        rawsamps = INPUT_STREAM.read(1024)
        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)

        # Show the volume and pitch
        loudness, pitch = (
            analyse.loudness(samps),
            analyse.musical_detect_pitch(samps)
        )

        # Visualize the volume and pitch.
        print loudness, pitch
        #show_loudness(loudness)

        if loudness > threshold:
            INPUT_STREAM.stop_stream()
            shush()
            INPUT_STREAM.start_stream()

if __name__ == '__main__':
    main()
