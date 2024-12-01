from Mode import Mode
import math
import numpy as np
class UniformMode(Mode):
    
    def __init__(self, sliders_widget,sample_instance, graph2,graph3, graph1, spectrogram_widget2,  num_of_sliders: int=10):
        super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2,graph3, spectrogram_widget2, graph1)
        self.freq_ranges = [[] for i in range (10)]
        self.sliders_values_array= np.ones(10)
        self.attenuation_array= None
       
    
    def init_mode(self):
        freq_list = self.sample.frequencies
        freq_list.sort()
        min_freq, max_freq = freq_list[0], freq_list[-1]
        total_range = max_freq - min_freq
        step_size = total_range / len(self.sliders_list)

        # Assign start and end points for each range
        for i in range(len(self.sliders_list)):
            range_start = min_freq + i * step_size
            range_end = min_freq + (i+1) * step_size  # Non-overlapping
            self.freq_ranges[i] = (range_start, range_end)  # Store as tuples
        
        self.update_slider_labels("Uniform",self.freq_ranges)

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        # Reset attenuation array
        self.attenuation_array = np.ones(len(freq_list))

        # Normalize slider values (assuming sliders go from 0 to 10)
        self.sliders_values_array = np.array([slider.value() /5 for slider in self.sliders_list])

        # Apply gain to frequencies in each range
        for i, (range_start, range_end) in enumerate(self.freq_ranges):
            self.attenuation_array = np.where(
                (freq_list >= range_start) & (freq_list <= range_end),
                self.attenuation_array * self.sliders_values_array[i],
                self.attenuation_array
            )

        # Apply attenuation to magnitudes
        new_freq_magnitude = (np.array(freq_mag) * self.attenuation_array).tolist()

        # Plot the updated Fourier domain
        self.plot_fourier_domain(freq_list, new_freq_magnitude)
        self.plot_inverse_fourier(new_freq_magnitude, freq_phase, self.time, self.graph2)


    
