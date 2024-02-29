import pylsl
import threading
from time import time, sleep
from matplotlib import pyplot as plt
import logging
import numpy
import sys
logging.basicConfig(level=logging.ERROR)


SECONDS_TO_RUN_TRIAL = 125
DEBUG_FLAG = 1


def send_test_streams(outlet_name, stop_event):
    # Send an LSL stream called outlet_name
    info = pylsl.StreamInfo(outlet_name, 'Markers', 1, 0, 'string', 'robot_input')
    outlet = pylsl.StreamOutlet(info)
    print('Sending test markers...')

    while not stop_event.is_set():
        outlet.push_sample(['Activated'])
        sleep(.4)
        outlet.push_sample(['Relaxed'])
        sleep(.2)


def send_2_test_streams(outlet_names, stop_event):
    # Send an LSL stream called outlet_name
    info = pylsl.StreamInfo(outlet_names[0], 'Markers', 1, 0, 'string', 'test1')
    outlet = pylsl.StreamOutlet(info)
    info = pylsl.StreamInfo(outlet_names[1], 'Markers', 1, 0, 'string', 'test2')
    outlet1 = pylsl.StreamOutlet(info)
    print('Sending 2 channel test markers...')

    while not stop_event.is_set():
        outlet.push_sample(['Activated'])
        sleep(.4)
        outlet1.push_sample(['Relaxed'])
        sleep(.2)


def test_lags(inlet_name: str, seconds: int = None, n_samples: int = 1000):
    if DEBUG_FLAG:
        print("Opening LSL output stream...")
        stop_event = threading.Event()
        send_test_streams_thread = threading.Thread(target=send_test_streams, args=(inlet_name, stop_event))
        send_test_streams_thread.start()

    stream = pylsl.resolve_stream('name', inlet_name)[0]
    inlet = pylsl.StreamInlet(stream)
    lags = []
    i = 0
    print("Recording lags...")
    end = time() + (seconds if seconds is not None else float('inf'))
    while time() < end and i < n_samples:
        sample, timestamp = inlet.pull_sample()
        if sample:
            lags.append(pylsl.local_clock() - timestamp)
        i += 1

    if DEBUG_FLAG:
        # Signal the sending thread to stop and wait for it to finish
        stop_event.set()
        send_test_streams_thread.join()

    return lags

def lags_get_info(lags):
    if lags:
        print('Mean lag: ', sum(lags) / len(lags))
        # TODO: FIX THIS random equation
        print('Standard deviation: ', numpy.std(lags))

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(lags, marker='o', linestyle='-', color='b')
        plt.title('LSL Stream Lags')
        plt.xlabel('Sample Index')
        plt.ylabel('Lag (seconds)')
        plt.grid(True)
        plt.show()
    else:
        print("No lags calculated, possibly no data received.")


def io_get_lag(inp_stream: str, out_stream: str, seconds: int = None, n_samples: int = 1000):
    if DEBUG_FLAG:
        print("Opening LSL output streams for testing...")
        stop_event = threading.Event()
        send_2_test_streams_thread = threading.Thread(target=send_2_test_streams, args=([inp_stream, out_stream], stop_event))
        send_2_test_streams_thread.start()

    print("Opening LSL output streams...")
    inp_stream = pylsl.StreamInlet(pylsl.resolve_stream('name', inp_stream)[0])
    out_stream = pylsl.StreamInlet(pylsl.resolve_stream('name', out_stream)[0])
    inps = []
    outs = []
    print("Recording lags...")
    end = time() + (seconds if seconds is not None else float('inf'))
    i = 0
    while time() < end and i < n_samples:
        sample, timestamp = inp_stream.pull_sample()
        if sample:
            inps.append(timestamp)
        sample, timestamp = out_stream.pull_sample()
        if sample:
            outs.append(timestamp)
        i += 1

    lags = [out - inp for inp, out in zip(inps, outs)]

    if DEBUG_FLAG:
        # Signal the sending thread to stop and wait for it to finish
        stop_event.set()
        send_2_test_streams_thread.join()

    return lags
"""
HOW TO TIME LAGS:
The LSL stream and script can have issues if the stream is not running when the script is run.
To test the lag between another LSL output and receiving on this machine, run 
    test_lags(INPUT-STREAM-NAME, seconds=SECONDS_TO_RUN_TRIAL(use this to end after n seconds), n_samples=100)
    Pass the result to lags_get_info() to get mean, stdev, and plot
To test the lag between two LSL outputs, run
    io_get_lag("INPUT-STREAM-NAME", seconds=SECONDS_TO_RUN_TRIAL, n_samples=100)
    These lags can also be passed to lags_get_info() to get mean, stdev, and plot
"""
if __name__ == '__main__':
    lags_get_info(io_get_lag('test_inp_stream', "test_out_stream", seconds=SECONDS_TO_RUN_TRIAL, n_samples=100))

