import threading
import sys
import sounddevice as sd
import numpy as np
from scipy.stats import mode

from bpm_detection import bpm_detector


class BPM:

    def __init__(self):
        self.bpm = 0.0
        self.recording_thread = None

        self.log_size = 5
        self.log = np.zeros(self.log_size)

    def calculate_bpm(self, fs=44100, seconds=3):
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        local_bpm, _ = bpm_detector(myrecording[:, 0], fs)
        try:
            local_bpm = local_bpm[0]
        except IndexError:
            return

        calculated_bpm = round(local_bpm, 1)
        self.update_log(calculated_bpm)

        mode_list, _ = mode(self.log)
        self.bpm = mode_list[0]

    def try_recording(self):
        thread = self.recording_thread
        if thread is None or not thread.is_alive():
            self.recording_thread = threading.Thread(target=self.calculate_bpm)
            self.recording_thread.start()

    def update_log(self, new_value):
        self.log = np.append(self.log[1:], new_value)

    def run(self):
        while True:
            self.try_recording()
            sys.stdout.flush()
            sys.stdout.write('\r' + str(self.bpm))


if __name__ == "__main__":
    BPM().run()
