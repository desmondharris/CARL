"""
Created 1/24//2024
Test the formatting and latency of OpenBCI LSL streaming from command line
"""
import pylsl
from time import sleep
stream = pylsl.resolve_stream('type', 'EEG')[0]
inlet = pylsl.StreamInlet(stream)
try:
    while True:
        sample, timestamp = inlet.pull_sample()
        print(timestamp, sample)
        sleep(1)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    exit(0)
