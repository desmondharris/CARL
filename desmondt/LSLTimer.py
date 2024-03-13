import pylsl
import threading
from time import time, sleep
from matplotlib import pyplot as plt
import logging
logging.basicConfig(level=logging.ERROR)


STREAM_NAME = 'ROBOT_INP'
SECONDS_TO_RUN_TRIAL = 100


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
    print('Sending test markers...')

    while not stop_event.is_set():
        outlet.push_sample(['Activated'])
        sleep(.4)
        outlet1.push_sample(['Relaxed'])
        sleep(.2)


def test_lags(inlet_name: str, seconds: int = None):
    print("Opening LSL output stream...")
    stop_event = threading.Event()
    send_test_streams_thread = threading.Thread(target=send_test_streams, args=(inlet_name, stop_event))
    send_test_streams_thread.start()

    stream = pylsl.resolve_stream('name', inlet_name)[0]
    inlet = pylsl.StreamInlet(stream)
    lags = []
    print("Recording lags...")
    end = time() + (seconds if seconds is not None else float('inf'))
    while time() < end:
        sample, timestamp = inlet.pull_sample()
        if sample:
            lags.append(pylsl.local_clock() - timestamp)

    # Signal the sending thread to stop and wait for it to finish
    stop_event.set()
    send_test_streams_thread.join()

    return lags

def main():
    lags = test_lags(STREAM_NAME, SECONDS_TO_RUN_TRIAL)
    if lags:
        print('Mean lag: ', sum(lags) / len(lags))
        print('Max lag: ', max(lags))
        print('Min lag: ', min(lags))
        print(lags)

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

if __name__ == '__main__':
    main()
