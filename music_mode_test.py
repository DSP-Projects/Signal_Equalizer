import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
import librosa
import numpy as np
import simpleaudio as sa
import pyqtgraph as pg
from scipy.fft import fft, ifft, fftfreq

# Load audio file using librosa
audio_file = "instument_mode.wav"  # Change to your file path
audio_data, sample_rate = librosa.load(audio_file, sr=None)  # Load with original sample rate

# Frequency bands in Hz
freq_bands = [(0, 170), (170, 250), (250, 400), (400, 1000)]
gains = [1.0] * len(freq_bands)  # Initial gains for each frequency band

# Function to apply equalization
def apply_equalizer(samples, sample_rate, gains):
    # Apply FFT to get frequency spectrum
    freqs = fftfreq(len(samples), 1 / sample_rate)  # Frequency bins corresponding to the FFT output
    spectrum = fft(samples)  # Perform FFT to get the spectrum

    # Apply gain to each frequency band
    for i, (low, high) in enumerate(freq_bands):
        # Select frequencies within each band
        band = (np.abs(freqs) >= low) & (np.abs(freqs) < high)
        spectrum[band] *= gains[i]  # Apply the gain to the selected frequency band

    # Apply inverse FFT to reconstruct the time-domain signal
    processed_samples = np.real(ifft(spectrum)).astype(np.float32)  # Convert back to time domain
    return processed_samples

# Function to play audio
def play_audio(samples, sample_rate):
    # Convert the processed samples to int16 format for playback
    samples_int16 = np.int16(samples * 32767)  # Normalize the samples to the int16 range
    audio_obj = sa.play_buffer(samples_int16, 1, 2, sample_rate)  # Play the audio using simpleaudio
    audio_obj.wait_done()  # Wait until playback finishes

class EqualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Equalizer")

        # Initialize gains attribute
        self.gains = [1.0] * len(freq_bands)

        # Layout setup
        layout = QVBoxLayout()

        # Original and Equalized play buttons
        self.play_original_button = QPushButton("Play Original")
        self.play_original_button.clicked.connect(lambda: play_audio(audio_data, sample_rate))
        layout.addWidget(self.play_original_button)

        self.play_equalized_button = QPushButton("Play Equalized")
        self.play_equalized_button.clicked.connect(self.play_equalized)
        layout.addWidget(self.play_equalized_button)

        # Sliders for each frequency range
        self.sliders = []
        for i, (low, high) in enumerate(freq_bands):
            label = QLabel(f"Gain for {low}-{high} Hz")
            layout.addWidget(label)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 200)  # Range for gain adjustment (0 to 2x gain)
            slider.setValue(100)  # Initial gain value (1.0)
            slider.valueChanged.connect(self.update_gain)
            layout.addWidget(slider)
            self.sliders.append(slider)

        # Graph plot for visualization
        self.graph_widget = pg.PlotWidget(title="Audio Waveform")
        layout.addWidget(self.graph_widget)
        self.update_graph(audio_data)

        # Main widget setup
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def update_gain(self):
        # Update gains based on slider positions
        for i, slider in enumerate(self.sliders):
            self.gains[i] = slider.value() / 100.0

    def play_equalized(self):
        # Apply equalizer and play the modified audio
        equalized_samples = apply_equalizer(audio_data, sample_rate, self.gains)
        self.update_graph(equalized_samples)
        play_audio(equalized_samples, sample_rate)

    def update_graph(self, data):
        # Plot the waveform data for visualization
        self.graph_widget.clear()
        time_axis = np.linspace(0, len(data) / sample_rate, num=len(data))  # Time axis for the graph
        self.graph_widget.plot(time_axis, data)  # Plot the audio waveform

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EqualizerApp()
    window.show()
    sys.exit(app.exec_())
