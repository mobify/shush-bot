import numpy
import analyse

from capture import INPUT_STREAM
from playback import shush
from visualize import show_loudness
from web_client import get_config

# App Constants
SHUSHBOT_ID = 1

def main():
    # Initial values.
    loudness = -40
    loop_count = 0

    threshold, volume = get_config(SHUSHBOT_ID);

    # Main control loop.
    while True:
        loop_count += 1

        # Read raw microphone data
        rawsamps = INPUT_STREAM.read(1024)
        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        # Show the volume and pitch
        loudness, pitch = (
            analyse.loudness(samps),
            analyse.musical_detect_pitch(samps)
        )

        # Poll for config changes.
        if loop_count % 100 == 0:
            print '\n\n Updating config...\n\n\n'
            # request new config and update.

        # Visualize the volume and pitch.
        print loudness, pitch
        show_loudness(loudness)

        if loudness > threshold:
            INPUT_STREAM.stop_stream()
            shush()
            INPUT_STREAM.start_stream()

if __name__ == '__main__':
    main()
