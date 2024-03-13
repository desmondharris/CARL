import tkinter as tk
from tkinter import ttk, font
from pylsl import StreamOutlet, StreamInfo
import threading
from time import sleep
import sys
import random

DEBUG = 1
TK_FNT_SIZE = 32
TIME_PER_LABEL = 3.5
N_SAMPLES = 4
PAUSE_EVERY = N_SAMPLES/4
if N_SAMPLES % 2 != 0:
    raise ValueError("N_SAMPLES must be even")

LABELS = {
    "UNI_RIGHT": ["RR", "RL"],
    "UNI_LEFT": ["LR", "LL"],
    "BI-ONEHAND": ["RR", "LL"],
    "BI-TWOHAND": ["BR", "BL"]
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
    def __init__(self, t_type: str, out_name: str):
        self.root = tk.Tk()
        if not DEBUG:
            pass
            self.root.attributes("-fullscreen", True)
        self.root.title("LSL Application")
        # Set a default window size (optional)
        self.root.geometry('800x600')
        self.root.bind('<Escape>', lambda e: self.root.iconify())

        self.display_frame = tk.Frame(self.root)

        # Add two columns labeled L and R
        self.r_frm = tk.Frame(self.display_frame)
        tk.Label(self.r_frm, text="\n\nRight Hand:\n\n",font=font.Font(family="Helvetica", size=TK_FNT_SIZE)).pack()
        self.right_hand_label = tk.Label(self.r_frm, text="RELAX", font=font.Font(family="Helvetica", size=TK_FNT_SIZE))
        self.right_hand_label.pack()
        self.r_frm.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.l_frm = tk.Frame(self.display_frame)
        tk.Label(self.l_frm, text="\n\nLeft Hand:\n\n",font=font.Font(family="Helvetica", size=TK_FNT_SIZE)).pack()
        self.left_hand_label = tk.Label(self.l_frm, text="RELAX", font=font.Font(family="Helvetica", size=TK_FNT_SIZE))
        self.left_hand_label.pack()
        self.l_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=80)

        # bottom widget
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.X, pady=(40, 10), expand=True)

        # Progress Bar setup
        self.progress = ttk.Progressbar(self.bottom_frame, orient="horizontal",
                                        length=800, mode="determinate")
        self.progress['maximum'] = TIME_PER_LABEL
        self.progress.pack(side=tk.TOP, fill=tk.X, expand=False, padx=85)

        # Show next prompt
        self.next_prompt = tk.Label(self.bottom_frame, text="", font=font.Font(family="Helvetica", size=TK_FNT_SIZE))
        self.next_prompt.pack(side=tk.TOP, fill=tk.X, expand=False, padx=10, pady=(0, 10))  # Adjusted padding for proximity

        TRIAL_TYPES = ["UNI_RIGHT", "UNI_LEFT", "BI-ONEHAND", "BI-TWOHAND"]
        self.trial_type = t_type
        if self.trial_type not in TRIAL_TYPES:
            raise ValueError(f"trial_type must be one of {TRIAL_TYPES}")

        # Create LSL outstream
        info = StreamInfo(name=out_name, type='Markers', channel_count=1, nominal_srate=0,
                          channel_format='string',
                          source_id='experimentdisplay')
        self.outlet = StreamOutlet(info)

    def launch_experiment(self):
        if not DEBUG:
            # Send warmup markers
            for _ in range(10):
                self.outlet.push_sample(['warmup'])
                sleep(1)
        # Create LSL outstream
        self.outlet.push_sample(['calib-begin'])

        lbls = [LABELS[self.trial_type][0]] * (int(N_SAMPLES / 2))
        [lbls.append(LABELS[self.trial_type][1]) for _ in range(int(N_SAMPLES / 2))]
        random.shuffle(lbls)

        for n in range(N_SAMPLES):
            # Remove last label
            choice = lbls.pop()
            # Shuffle labels
            random.shuffle(lbls)
            if DEBUG:
                print(choice)
                print(lbls, end="\n\n")
            if n % PAUSE_EVERY == 0 and n != 0 and n != N_SAMPLES - 1 and not DEBUG:
                self.right_hand_label.config(text="PAUSE")
                self.left_hand_label.config(text="PAUSE")
                granularity = 0.005
                for t in range(int(10.0 / .005)):  # Multiply by 10 for a 0.1 second granularity
                    self.update_progress_bar(((granularity*t)/10)*TIME_PER_LABEL)  # Update progress bar value
                    sleep(0.005)  # Wait for 0.1 second before updating again
            else:
                # hand is first symbol, direction is second symbol
                hand, direction = choice[0], choice[1]
                # CHANGE SYMBOLS HERE
                if hand == "R":
                    self.right_hand_label.config(text="==>" if direction == "R" else "<==")
                    self.left_hand_label.config(text="RELAX")
                elif hand == "L":
                    self.left_hand_label.config(text="==>" if direction == "R" else "<==")
                    self.right_hand_label.config(text="RELAX")
                elif hand == "B":
                    direction = " ==> " if direction == "R" else " <== "
                    self.left_hand_label.config(text=direction)
                    self.right_hand_label.config(text=direction)
                self.outlet.push_sample([choice])
                for t in range(int(TIME_PER_LABEL * 200)):  # Multiply by 10 for a 0.1 second granularity
                    self.update_progress_bar(t / 200)  # Update progress bar value
                    sleep(0.005)  # Wait for 0.1 second before updating again
                # Brief pause
                self.right_hand_label.config(text="")
                self.left_hand_label.config(text="")
                # if len(lbls) > 0:
                #     if (n+1)%PAUSE_EVERY == 0:
                #         self.next_prompt.config(text="NEXT:  PAUSE")
                #     else:
                #         self.next_prompt.config(text=f"\n\nNEXT: {dir_dict[lbls[-1][0]]} hand: {dir_dict[lbls[-1][1]]} turn")
                # else:
                #     self.next_prompt.config(text="\n\nNEXT: END")
                sleep(1)
                self.next_prompt.config(text="")
        self.outlet.push_sample(['calib-end'])

        # Close tkinter window
        #self.root.destroy()

    def update_progress_bar(self, value):
        """Update the progress bar value."""
        self.progress['value'] = value
        self.root.update_idletasks()  # Update the GUI

    def start(self):
        # Launch the experiment
        exp_thread = threading.Thread(target=self.launch_experiment)
        exp_thread.daemon = True
        exp_thread.start()

        # Start the Tkinter event loop
        self.root.mainloop()

        # Clean up
        print("Exiting...")

if __name__ == "main":
    app = None
