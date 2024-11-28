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
            self.freq_ranges['piano'] =  [(0,10), (250, 275), (505, 540), (780, 790),(1040, 1060), (1565, 1590), (1840, 1850),(2105, 2120), (2375, 2395), (2650, 2665), (2925, 2940), (3200, 3215), (3487,3491), (3770, 3780), (4345, 4355), (4638, 4656), (4900, 4980)]
            self.freq_ranges['violin'] =  [(1020, 1060), (1520, 1600), (2560, 2640), (3080, 3180), (3590, 3720),(4110,4230),(4640,4650), (5140,5345)]
            self.freq_ranges['triangle'] =  [(4600, 5000), (5170, 5250), (5350, 5550), (5600,22000)]
            self.freq_ranges['xilaphone'] =  [(300,1000)]
            self.update_slider_labels("Instrument")
            
            self.sliders_values_array= np.ones(4)


    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        """
        Update the frequency magnitudes based on slider changes, preserving cumulative effects of all sliders.
        """
        instruments = ['piano', 'violin', 'triangle', 'xilaphone']
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
