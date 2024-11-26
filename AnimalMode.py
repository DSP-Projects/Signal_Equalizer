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
            self.sliders_values_array= np.ones(4)
            
            

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
               
        attenuation_array= np.ones(len(freq_mag))
        print(f"len(attenuation_array): {len(attenuation_array)}")

        for slider_num,slider in enumerate(self.sliders_list):
            self.sliders_values_array[slider_num]= (slider.value() /5)
        print(f"self.sliders_values_array: {self.sliders_values_array}")

        # Apply gain only to frequencies within the specified range
        for i, freq_range in enumerate (self.freq_ranges):
            attenuation_array = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                    attenuation_array * self.sliders_values_array[i], 
                                    attenuation_array)
            
        new_freq_mag= freq_mag.copy()
        print(type(new_freq_mag), type(freq_mag))
        new_freq_mag= (freq_mag * attenuation_array)
        
        print(f"new_freq_mag match freq_mag: {(np.array_equal(new_freq_mag, freq_mag))} ")

        print(f"len(new_freq_mag): {len(new_freq_mag)}")
        new_freq_mag= new_freq_mag.tolist()
        # Plot the updated frequency domain
        self.plot_fourier_domain(freq_list, new_freq_mag)
        self.plot_inverse_fourier(new_freq_mag, freq_phase, self.time, self.graph2)

                        