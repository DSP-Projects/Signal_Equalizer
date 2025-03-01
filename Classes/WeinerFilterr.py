from Classes.Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow ,QMessageBox, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from pyqtgraph import GraphicsLayoutWidget, RectROI
import pyqtgraph as pg
from Classes.Graph import Graph
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, istft, butter, lfilter,resample
import matplotlib.pyplot as plt
from Classes.Spectrogram import Spectrogram

from Signal import Signal
class WeinerFilterr(Mode):
    def __init__(self, sliders_widget, sample_rate, graph2, graph3, graph1, spectrogram_widget2, graph_widget, signal, num_of_sliders: int=0):
        super().__init__(sliders_widget, num_of_sliders, sample_rate, graph2, graph3, spectrogram_widget2, graph1)
        self.sliders_widget = sliders_widget
        self.num_of_sliders = num_of_sliders
        self.graphWidget = graph_widget
        self.clear_button = QPushButton("Clear")
        self.select_button = QPushButton("Select")
        self.graph1 = graph1
        self.signal = signal
        self.noisy_signal=None
        self.rectangle = None
        #self.noisy_signal = None  # To store the uploaded signal
        self.noise_signal = None  # To store the extracted noise signal
        self.filtered_signal = None
        self.samplerate=sample_rate
        self.spectrogram_widget2=spectrogram_widget2
        self.spectrogram_output = Spectrogram()
       # self.fs, self.noise_signal = wavfile.read("C:/dsp_task_3/Signal_Equalizer-/ambient-noise-VEED.wav")
        button_style = """
            QPushButton {
                background-color: #3388b0;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2d77a0;
            }
            QPushButton:pressed {
                background-color: #24688c;
            }
        """
        self.clear_button.setStyleSheet(button_style)
        self.select_button.setStyleSheet(button_style)

        layout = self.sliders_widget.layout()

        # Add buttons to the layout
        layout.addWidget(self.select_button)
        layout.addWidget(self.clear_button)

        # Connect buttons to their respective functionalities
        self.clear_button.clicked.connect(self.clear_region)
        self.select_button.clicked.connect(self.select_region)

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
       pass
      
 


    def set_signal(self,signal):
        self.signal=signal
    def clear_region(self):
        """Extract data from the rectangular region and apply Wiener filtering."""
        if not self.rectangle:
            QMessageBox.warning(None, "Clear Action", "No rectangle exists to extract data from.")
            return

        pos = self.rectangle.pos()
        size = self.rectangle.size()
        x_min, x_max = pos.x(), pos.x() + size.x()

        if self.signal.signal_data_time is None or self.signal.signal_data_amplitude is None:
            QMessageBox.warning(None, "Clear Action", "No signal data available to filter.")
            return

        time_data = np.array(self.signal.signal_data_time, dtype=np.float64)
        amplitude_data = np.array(self.signal.signal_data_amplitude, dtype=np.float64)
        
        self.noisy_signal = self.signal.get_signal()
        print(f"Original signal length in clear: {len(self.noisy_signal)}")


        indices = np.where((time_data >= x_min) & (time_data <= x_max))[0]
        if len(indices) == 0:
            QMessageBox.warning(None, "Clear Action", "No data found in the selected rectangle.")
            return

        self.noise_signal = amplitude_data[indices]  # Extract noise signal
        print(f"noise signal length: {len(self.noise_signal)}")
        if self.noisy_signal.ndim > 1:
            self.noisy_signal = self.noisy_signal[:, 0]
        if self.noise_signal.ndim > 1:
           self. noise_signal =self. noise_signal[:, 0]
        denoised_signal, freq_list, freq_mag, freq_phase  = self.wiener_filter_fft(
            self.noisy_signal, self.noise_signal,self.signal.sample_rate
        )

        if denoised_signal is None:
            QMessageBox.warning(None, "Filtering Error", "The filtering process failed.")
            return
        self.plot_inverse_fourier(freq_mag, freq_phase, time_data, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag)

        self.graphWidget.removeItem(self.rectangle)
        self.rectangle = None

    def select_region(self):
        """Add a resizable rectangle to graph1."""
        if not self.rectangle:
            self.rectangle = RectROI([0, 0], [0.01, 0.01], pen=pg.mkPen(color='r', width=2))
            self.rectangle.addScaleHandle((1, 1), (0, 0))
            self.rectangle.addScaleHandle((0, 0), (1, 1))
            self.rectangle.addScaleHandle((0, 1), (1, 0))
            self.rectangle.addScaleHandle((1, 0), (0, 1))
            self.graphWidget.addItem(self.rectangle)
            self.rectangle.sigRegionChanged.connect(self.on_region_changed)

        QMessageBox.information(None, "Select Action", "Rectangle added to Graph1! You can resize or move it.")

    def on_region_changed(self):
        """Log changes to the ROI."""
        if self.rectangle:
            pos = self.rectangle.pos()
            size = self.rectangle.size()
            #print(f"Rectangle position: {pos}, size: {size}")
    def wiener_filter_fft(self,noisy_signal, noise_signal, fs, n_fft=1024, overlap=None, iterations=5, spectral_floor=0.00001):

     if noisy_signal is None or len(noisy_signal) == 0:
            raise ValueError("Error: noisy_signal is None or empty.")

     if noise_signal is None or len(noise_signal) == 0:
            raise ValueError("Error: noise_signal is None or empty.")

     noisy_signal = np.asarray(noisy_signal)
     noise_signal = np.asarray(noise_signal)

     if noisy_signal.ndim != 1:
            raise ValueError(f"Expected 1D noisy_signal, but got shape {noisy_signal.shape}")
        
     if noise_signal.ndim != 1:
            raise ValueError(f"Expected 1D noise_signal, but got shape {noise_signal.shape}")
     if overlap is None or overlap >= n_fft:
        overlap = n_fft // 2
     
    # wavfile.write('noisy_audio_iterative.wav', int(fs), noisy_signal.astype(np.int16))
    # wavfile.write('noise_audio_iterative.wav', int(fs), noise_signal.astype(np.int16))
    # Perform STFT on noisy and noise signals
     freqs, _, noisy_stft = stft(noisy_signal, fs, nperseg=n_fft, noverlap=overlap)  
     _, _, noise_stft = stft(noise_signal, fs, nperseg=n_fft, noverlap=overlap)  
    
    # Compute Noise PSD (Power Spectral Density)
     noise_psd = np.mean(np.abs(noise_stft) ** 2, axis=-1, keepdims=True)

    # Filter the noisy signal in the frequency domain
     filtered_stft = noisy_stft
     for _ in range(iterations):  # Increasing iterations
        noisy_psd = np.abs(filtered_stft) ** 2
        wiener_filter = np.maximum(noisy_psd / (noisy_psd + noise_psd), spectral_floor)
        filtered_stft = wiener_filter * noisy_stft

    # Reconstruct the denoised signal using ISTFT
     _, denoised_signal = istft(filtered_stft, fs, nperseg=n_fft, noverlap=overlap) 
     denoised_signal = np.nan_to_num(denoised_signal)
    # wavfile.write('denoised_audio_iterative.wav', int(fs), denoised_signal.astype(np.int16)) # Using 'hann' window
     N = len(denoised_signal)  
     freq_list = np.fft.fftfreq(N, d=1/fs)  # Frequency bins
     fft_values =np.fft.fft(denoised_signal)  # Compute FFT
     freq_mag = np.abs(fft_values)  # Magnitude Spectrum
     freq_phase = np.angle(fft_values) 
     return  denoised_signal, freq_list[:N//2], freq_mag[:N//2], freq_phase[:N//2]
    

