import numpy
import analyse

from capture import INPUT_STREAM


def main():
    while True:
        # Read raw microphone data
        rawsamps = INPUT_STREAM.read(1024)
        # Convert raw data to NumPy array
        samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
        # Show the volume and pitch
        print analyse.loudness(samps), analyse.musical_detect_pitch(samps)


if __name__ == '__main__':
    main()