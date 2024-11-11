import pandas as pd
import matplotlib.pyplot as plt

# Load ECG data from CSV files
normal_signal = pd.read_csv('normal.csv')
af_signal = pd.read_csv('Atrial fibrillation.csv')
brady_signal = pd.read_csv('Bradycardia.csv')
vt_signal = pd.read_csv('Ventricular tachycardia.csv')

# Ensure all signals are of the same length
min_length = min(len(normal_signal), len(af_signal), len(brady_signal), len(vt_signal))

# Truncate signals to the minimum length and limit to the first 1000 points
n_points = 2000
normal_signal = normal_signal[:min(n_points, min_length)]
af_signal = af_signal[:min(n_points, min_length)]
brady_signal = brady_signal[:min(n_points, min_length)]
vt_signal = vt_signal[:min(n_points, min_length)]

# Combine the Amplitude columns
combined_amplitude = (normal_signal['Amplitude'] +
                      af_signal['Amplitude'] +
                      brady_signal['Amplitude'] +
                      vt_signal['Amplitude'])

# Create a time vector for the combined signal
time_vector = normal_signal['Time'][:min(n_points, min_length)]

# Set up the figure and axes for 5 subplots
fig, axs = plt.subplots(5, 1, figsize=(12, 18), sharex=True)

# Plot each individual signal
axs[0].plot(normal_signal['Time'], normal_signal['Amplitude'], label='Normal', color='green')
axs[0].set_title('Normal ECG Signal')
axs[0].set_ylabel('Amplitude')
axs[0].grid()

axs[1].plot(af_signal['Time'], af_signal['Amplitude'], label='Atrial Fibrillation', color='red')
axs[1].set_title('Atrial Fibrillation ECG Signal')
axs[1].set_ylabel('Amplitude')
axs[1].grid()

axs[2].plot(brady_signal['Time'], brady_signal['Amplitude'], label='Bradycardia', color='orange')
axs[2].set_title('Bradycardia ECG Signal')
axs[2].set_ylabel('Amplitude')
axs[2].grid()

axs[3].plot(vt_signal['Time'], vt_signal['Amplitude'], label='Ventricular Tachycardia', color='purple')
axs[3].set_title('Ventricular Tachycardia ECG Signal')
axs[3].set_ylabel('Amplitude')
axs[3].grid()

# Plot the combined signal
axs[4].plot(time_vector, combined_amplitude, label='Combined ECG Signal', color='blue')
axs[4].set_title('Combined ECG Signal from Multiple Sources')
axs[4].set_xlabel('Time')
axs[4].set_ylabel('Amplitude')
axs[4].grid()

# Adjust layout
plt.tight_layout()
plt.show()