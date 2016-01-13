import numpy
import analyse

from capture import INPUT_STREAM
from playback import shush

loudness = -40


def main():
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

        # Show the volume and pitch
        # print loudness

        if loudness > -7:
            INPUT_STREAM.stop_stream()
            shush()
            INPUT_STREAM.start_stream()

if __name__ == '__main__':
    main()