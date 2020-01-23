import sounddevice as sd
from scipy.io.wavfile import write
from bpm_detection import bpm_detector
import numpy as np
from scipy.stats import mode

fs = 44100  # Sample rate
seconds = 3 # Duration of recording
log_size = 5 # Number of previous measurements used



log = np.zeros(log_size)
last_printed = 0.0

while True:
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    bpm, correl = bpm_detector(myrecording[:,0], fs)
    try:
        bpm = bpm[0]
    except:
        bpm = 0.0

    bpm = round(bpm, 3)
    log = np.append(log[1:],bpm)

    bpm, count = mode(log)
    bpm = bpm[0]
    print(bpm)