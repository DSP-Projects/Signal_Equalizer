from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class MusicMode(Mode):
    
    def __init__(self, sliders_widget, sample_instance, graph2,graph3, graph1,spectrogram_widget2, num_of_sliders: int=4):
            super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2, graph3, spectrogram_widget2, graph1)
            self.old_value=5
            self.freq_ranges=dict()
            self.freq_ranges['drums'] =  [(20,260)]
            self.freq_ranges['letter s'] =  [(2000,15000)]
            self.freq_ranges['letter I'] =  [(650,1700)]
            self.freq_ranges['Triangle'] =  [(4000,19000)]
            self.update_slider_labels("Instrument")
            
            self.sliders_values_array= np.ones(4)


    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        """
        Update the frequency magnitudes based on slider changes, preserving cumulative effects of all sliders.
        """
        instruments = ['drums', 'letter s', 'letter I', 'Triangle']
        if slider_index >= len(instruments):
                return  # Invalid slider index

        # Reset attenuation array to recompute effects from all sliders
        attenuation_array = np.ones(len(freq_list))
        print(f"len(attenuation_array): {len(attenuation_array)}")

        # Update sliders' gain values
        for slider_num, slider in enumerate(self.sliders_list):
                self.sliders_values_array[slider_num] = slider.value() / 5

        print(f"self.sliders_values_array: {self.sliders_values_array}")

        # Apply cumulative attenuation based on all sliders
        for i, (instrument_key, freq_ranges) in enumerate(self.freq_ranges.items()):
                for freq_range in freq_ranges:
                        attenuation_array = np.where(
                                (freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                attenuation_array * self.sliders_values_array[i],
                                attenuation_array
                        )

        # Update frequency magnitudes with the cumulative attenuation
        new_freq_mag = freq_mag * attenuation_array

        # Plot the updated frequency domain
        self.plot_fourier_domain(freq_list, new_freq_mag)
        self.plot_inverse_fourier(new_freq_mag, freq_phase, self.time, self.graph2)
