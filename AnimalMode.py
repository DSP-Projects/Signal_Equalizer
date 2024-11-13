from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class AnimalMode(Mode):
    
    def __init__(self, sliders_widget,sample_instance,graph2,graph3, graph1, spectrogram_widget2,  num_of_sliders: int=4):
            super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2,graph3, spectrogram_widget2,graph1)
            # Dogs   ,    Wolves    ,   Crow    ,     Bat 
            self.freq_ranges =  [(0, 450), (450, 1100), (1100, 3000), (3000, 9000)]
            self.old_value= 5
            

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        gain_factor = gain_value/self.old_value # to handle slider values correctly 
        self.old_value= gain_value # Normalize gain to a 0-2 factor

        # Get the frequency range for this slider
        freq_range = self.freq_ranges[slider_index]

        # Apply gain only to frequencies within the specified range
        freq_mag_modified = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                freq_mag * gain_factor, 
                                freq_mag)
        
        # Plot the updated frequency domain
        self.plot_inverse_fourier(freq_mag_modified, freq_phase, self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag_modified)
                        