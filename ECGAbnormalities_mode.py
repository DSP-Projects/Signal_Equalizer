from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class ECGAbnormalities(Mode):
    def __init__(self, sliders_widget, sample_instance,graph2,graph3, graph1, spectrogram_widget2,  num_of_sliders=4):
        super().__init__(sliders_widget, num_of_sliders, sample_instance, graph2,graph3, spectrogram_widget2, graph1)
        self.sliders_widget = sliders_widget
        self.num_of_sliders = num_of_sliders
        
        # Define frequency ranges for each ECG abnormality
        self.freq_ranges = {
            0: (0, 50),        # Normal range
            1: (0, 7),         # Atrial fibrillation range
            2: (0, 0.5),       # Bradycardia range
            3: (3, 10)         # Ventricular tachycardia range
        }
        
    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        gain_factor = (gain_value / max(self.gain_limits)) * 2  # Normalize gain to a 0-2 factor

        # Get the frequency range for this slider
        freq_range = self.freq_ranges[slider_index]

        # Apply gain only to frequencies within the specified range
        freq_mag = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                freq_mag * gain_factor, 
                                freq_mag)
        
        # Plot the updated frequency domain
        self.plot_inverse_fourier(freq_mag, freq_phase, self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag)


    