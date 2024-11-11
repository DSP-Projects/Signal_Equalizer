from Mode import Mode
import math
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
            for comp in freq_list:
                if comp in range(range_start,range_end):
                    self.freq_ranges[i].append(comp)
                elif comp > range_end:
                     break

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        gain_factor = (gain_value / max(self.gain_limits))*2  # Normalize gain to a 0-2 factor
        # Apply gain to the frequencies in this range 
        freq_mag= [freq*gain_factor for freq in freq_mag if freq_list.index(freq) in range(self.freq_ranges[slider_index])]
        self.plot_inverse_fourier(freq_mag,freq_phase,self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag)
