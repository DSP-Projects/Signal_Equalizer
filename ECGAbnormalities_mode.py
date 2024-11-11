from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class ECGAbnormalities(Mode):
    def __init__(self, sliders_widget, sample_instance,graph2,graph3,  num_of_sliders=4):
        super().__init__(sliders_widget, num_of_sliders, sample_instance, graph2,graph3)
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
       
        # Calculate gain factor from the slider value (normalized to 0-2 range)
        gain_factor = (gain_value / 50)  # Normalizing around 1x default
        
        # Get the frequency range for the specified slider index
        low_freq, high_freq = self.freq_ranges.get(slider_index, (0, 0))
        
        # Apply gain factor to the frequency components in the specified range
        for i, freq in enumerate(freq_list):
            if low_freq <= abs(freq) <= high_freq:
                freq_mag[i] *= gain_factor
        self.plot_inverse_fourier(self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag)
    


    