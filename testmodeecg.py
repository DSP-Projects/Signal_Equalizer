import sys
import numpy as np
import pandas as pd
from scipy.fft import fft, ifft, fftfreq
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

class SignalEqualizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the original signal from the CSV file
        self.original_signal = self.load_signal(r'C:/dsp_task_3/Signal_Equalizer-/combined_signal.csv')
        
        # Set up sample rate and signal duration based on the loaded signal
        self.sample_rate = 1000  # Hz
        self.signal_duration = len(self.original_signal) / self.sample_rate
        self.signal_time = np.linspace(0, self.signal_duration, len(self.original_signal))
        
        # Copy the original signal to the modified signal
        self.modified_signal = self.original_signal.copy()

        # Set up UI components
        self.setWindowTitle("Signal Equalizer")
        self.setGeometry(100, 100, 1000, 600)

        # Create viewers for input and output signals
        self.input_viewer = self.create_viewer("Input Signal")
        self.output_viewer = self.create_viewer("Output Signal")
        
        # Synchronize the two viewers
        self.input_viewer.sigXRangeChanged.connect(self.sync_viewers)
        self.output_viewer.sigXRangeChanged.connect(self.sync_viewers)
        
        # Layout for sliders and buttons
        self.controls_layout = QtWidgets.QVBoxLayout()
        
        # Slider to adjust arrhythmia component magnitudes
        self.sliders = []
        arrhythmia_types = ['Normal', 'Atrial fibrillation', 'Bradycardia', 'Ventricular tachycardia']
        for i, arrhythmia in enumerate(arrhythmia_types):
            slider = self.create_slider(f"{arrhythmia} Magnitude")
            slider.valueChanged.connect(self.update_frequency_component)
            self.controls_layout.addWidget(slider)
            self.sliders.append(slider)
        
        # Play controls for cine viewer synchronization
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.play_signal)
        self.controls_layout.addWidget(self.play_button)
        
        self.pause_button = QtWidgets.QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_signal)
        self.controls_layout.addWidget(self.pause_button)
        
        # Set up central layout
        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        
        # Left panel (controls)
        controls_widget = QtWidgets.QWidget()
        controls_widget.setLayout(self.controls_layout)
        
        # Right panel (input and output viewers)
        viewers_layout = QtWidgets.QVBoxLayout()
        viewers_layout.addWidget(self.input_viewer)
        viewers_layout.addWidget(self.output_viewer)
        
        main_layout.addWidget(controls_widget)
        main_layout.addLayout(viewers_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Timer for play functionality
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.advance_viewers)

    def create_viewer(self, title):
        viewer = pg.PlotWidget(title=title)
        viewer.plot(self.signal_time, self.original_signal, pen="b")
        return viewer

    def create_slider(self, label):
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setToolTip(label)
        return slider

    def load_signal(self, file_path):
        # Load combined ECG signal from CSV file
        df = pd.read_csv(file_path, skiprows=1, header=None)
        signal = pd.to_numeric(df.iloc[:, 1], errors='coerce').dropna().values
        return signal

    def sync_viewers(self):
        """Ensure both viewers show the same time range."""
        input_range = self.input_viewer.viewRange()[0]
        self.output_viewer.setXRange(*input_range, padding=0)

    def update_frequency_component(self):
        """Recalculate and plot the output signal with modified frequency components."""
        # Apply FFT to the original signal
        fft_result = fft(self.original_signal)
        freqs = fftfreq(len(fft_result), d=1/self.sample_rate)

        # Define frequency ranges for each arrhythmia type
        arrhythmia_ranges = {
            'Normal': (0, 50),
            'Atrial fibrillation': (0, 7),
            'Bradycardia': (0, 0.5),
            'Ventricular tachycardia': (3, 10)
        }

        # Adjust magnitudes based on slider values
        for i, (arrhythmia, (low_freq, high_freq)) in enumerate(arrhythmia_ranges.items()):
            scale_factor = self.sliders[i].value() / 50  # Scale component around 1x (default)
            # Apply to specific frequency bands
            indices = np.where((freqs >= low_freq) & (freqs <= high_freq))
            fft_result[indices] *= scale_factor

        # Inverse FFT to get modified signal
        self.modified_signal = np.real(ifft(fft_result))
        
        # Update the output viewer
        self.output_viewer.clear()
        self.output_viewer.plot(self.signal_time, self.modified_signal, pen="r")

    def play_signal(self):
        self.timer.start(50)  # Adjust time interval as needed

    def pause_signal(self):
        self.timer.stop()

    def advance_viewers(self):
        """Advance the view for the play function."""
        current_range = self.input_viewer.viewRange()[0]
        step = (self.signal_time[-1] - self.signal_time[0]) / 50
        self.input_viewer.setXRange(current_range[0] + step, current_range[1] + step, padding=0)

# Main function to start the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SignalEqualizer()
    mainWin.show()
    sys.exit(app.exec_())
