import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Load the audio file
sample_rate, signal = wavfile.read('instument_mode.wav')
print(signal.shape)
# Convert sample indices to time (in seconds)
duration = len(signal) / sample_rate  # Total duration in seconds
time = np.linspace(0, duration, len(signal))  # Time array based on sample rate

# Plotting the waveform
plt.figure(figsize=(10, 4))
plt.plot(time, signal, color="blue")
plt.title("Audio Signal Waveform")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
