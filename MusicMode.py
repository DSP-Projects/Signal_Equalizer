from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class MusicMode(Mode):
    
    def __init__(self, sliders_widget, num_of_sliders: int=4):
            super().__init__(sliders_widget, num_of_sliders)
            self.freq_ranges =  [(0, 170), (170, 250), (250, 400), (400, 1000)]
            

    def init_mode(self, freq_list):
           pass
        
    def update_mode_upon_sliders_change(self, slider_index, gain_value,freq_list, freq_mag,freq_phase):
            gain_factor = (gain_value / max(self.gain_limits))*2  # Normalize gain to a 0-2 factor
            # Apply gain to the frequencies in this range 
            freq_mag = [freq*gain_factor for freq in freq_mag if freq_list.index(freq) in range(self.freq_ranges[slider_index])]
            signal= self.send_reconstruct(freq_mag, freq_phase)
            return signal
                        
                   
                   
                
 