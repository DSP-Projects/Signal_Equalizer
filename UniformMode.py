from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
from PyQt5.QtCore import Qt

class UniformMode(Mode):
    
    def __init__(self, sliders_widget, num_of_sliders: int=10):
        super().__init__(sliders_widget, num_of_sliders)
        self.freq_ranges = [[] for i in range (10)]
        
    
    def init_mode(self, freq_list):
        # Sort frequencies and determine ranges
        freq_list.sort()
        min_freq, max_freq = freq_list[0], freq_list[-1]
        total_range = max_freq - min_freq
        step_size = total_range / len(self.sliders_list)
        
        # Assign frequencies to corresponding ranges
        for i in range(10): 
            range_start = int(min_freq + i * step_size)
            range_end = int(range_start + step_size)
            for comp in freq_list:
                if comp in range(range_start,range_end):
                    self.freq_ranges[i].append(comp)
                elif comp > range_end:
                     break

    def update_mode_upon_sliders_change(self, slider_index, gain_value):
        gain_factor = (gain_value / max(self.gain_limits))*2  # Normalize gain to a 0-2 factor
        # Apply gain to the frequencies in this range 
        self.freq_ranges[slider_index]= [freq*gain_factor for freq in self.freq_ranges[slider_index]]
        return self.freq_ranges
    
# if __name__== '__main__':
#     import numpy as np
#     list_freq= [0, 10, 20, 50, 60, 70, 80, 90, 100, 200]
#     app = QApplication(sys.argv)
#     widget= QWidget()
#     uniform= UniformMode(widget)
#     uniform.init_mode(list_freq)
#     print(uniform.update_mode_upon_sliders_change(1, 10))