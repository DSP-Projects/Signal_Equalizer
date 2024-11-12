from Mode import Mode
import math
import numpy as np
class UniformMode(Mode):
    
    def __init__(self, sliders_widget,sample_instance, graph2,graph3,  num_of_sliders: int=10):
        super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2,graph3)
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
            print(f"range_start, range_end{range_start, range_end}")
            for comp in freq_list:
                if range_start <= comp < range_end:
                    self.freq_ranges[i].append(comp)
                elif comp > range_end:
                     break

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        self.init_mode(freq_list)
        #print(self.freq_ranges)
        gain_factor = (gain_value / max(self.gain_limits)) * 5  # Normalize gain to a 0-2 factor
        # Get the frequency range for this slider
        freq_range = self.freq_ranges[slider_index]
        print(f"freq_mag before{freq_mag}")
        # Apply gain only to frequencies within the specified range
        freq_mag = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                freq_mag * gain_factor, 
                                freq_mag)
        print(f"freq_mag after{freq_mag}")
        # Plot the updated frequency domain
        self.plot_inverse_fourier(freq_mag, freq_phase, self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag)
