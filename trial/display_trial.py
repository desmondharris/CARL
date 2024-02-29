import tkinter as tk
from pylsl import StreamInlet, StreamOutlet, StreamInfo, resolve_stream
import threading
from time import sleep, time

DEBUG = 1

TRIAL_TYPES = ["UNI_RIGHT", "UNI_LEFT", "BI"]
TRIAL_TYPE = TRIAL_TYPES[0]
OUTPUT_STREAM_NAME = "curl_relax_markers"
TIME_PER_LABEL = 3.5
N_SAMPLES = 10
LABELS = {
    "UNI_RIGHT": ["RR", "RL"],
    "UNI_LEFT": ["LR", "LL"],
    "BI": ["BR", "BL"]
}


def send_test_streams(outlet_name):
    # Send an LSL stream called outlet_name
    info = StreamInfo(outlet_name, 'Markers', 1, 0, 'string', 'robot_input')
    outlet = StreamOutlet(info)
    print('Sending test markers...')

    while True:
        outlet.push_sample(['Activated'])
        sleep(.4)
        outlet.push_sample(['Relaxed'])
        sleep(.2)


class LSLApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LSL Application")
        # Set a default window size (optional)
        self.root.geometry('800x600')
        self.root.bind('<Escape>', lambda e: self.root.quit())

        # Add two columns labeled L and R
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.display_label = tk.Label(self.display_frame, text="LEFT:    RIGHT:         ")
        self.display_label.pack()

        # Create LSL outstream
        info = StreamInfo(name=OUTPUT_STREAM_NAME, type='Markers', channel_count=1, nominal_srate=0,
                          channel_format='string',
                          source_id='experimentdisplay')
        self.outlet = StreamOutlet(info)

    def launch_experiment(self):
        # Create LSL outstream
        self.outlet.push_sample(['calib-begin'])
        for _ in range(N_SAMPLES):
            choice = int(time() * 10) % 2
            symbol_dict = {
                "RL": "Right hand:  Rotate left  \n\n Left hand: RELAX",
                "RR": "Right hand:  Rotate right \n\n Left hand: RELAX",
                "LR": "Right hand:  RELAX\n\n Left hand: Rotate right",
                "LL": "Right hand:  RELAX\n\n Left hand: Rotate left",
            }
            self.display_label.config(text=symbol_dict[LABELS[TRIAL_TYPE][choice]])
            self.outlet.push_sample([LABELS[TRIAL_TYPE][choice]])
            sleep(TIME_PER_LABEL)
        self.outlet.push_sample(['calib-end'])

        # Close tkinter window
        self.root.destroy()


    def start(self):
        # Launch the experiment
        exp_thread = threading.Thread(target=self.launch_experiment)
        exp_thread.daemon = True
        exp_thread.start()

        # Start the Tkinter event loop
        self.root.mainloop()

        # Clean up
        print("Exiting...")
        self.outlet.push_sample(['calib-end'])


app = LSLApp()

app.start()

