from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class ECGAbnormalities(Mode):
    def __init__(self, sliders_widget,sample_instance, graph2,graph3, graph1, spectrogram_widget2,  num_of_sliders: int=4):
        super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2,graph3, spectrogram_widget2, graph1)
        self.sliders_widget = sliders_widget
        self.num_of_sliders = num_of_sliders
        self.sliders_values_array= np.ones(4)
        self.attenuation_array= None
        self.update_slider_labels("ECG")
        
        # Define specific frequency values for each ECG abnormality
        self.freq_ranges = [
            [0,50],        # Normal range
           [50,100],         # Atrial fibrillation range
             [95, 249],       # Ventricular tachycardia range
            [141, 190]         # Bradycardia range
        ]
        print('range done')
    
    
    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        
        self.attenuation_array= np.ones(len(self.sample.magnitudes))

        for slider_num,slider in enumerate(self.sliders_list):
            self.sliders_values_array[slider_num]=(slider.value())

        # Apply gain only to frequencies within the specified range
        for i, freq_range in enumerate (self.freq_ranges):
            self.attenuation_array = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                    self.attenuation_array * self.sliders_values_array[i], 
                                    self.attenuation_array)
        
        freq_mag= np.array(freq_mag)
        new_freq_magnitude= (freq_mag*self.attenuation_array).tolist()
        
        # Plot the updated frequency domain
        self.plot_inverse_fourier(new_freq_magnitude, freq_phase, self.time, self.graph2)
        self.plot_fourier_domain(freq_list, new_freq_magnitude)
