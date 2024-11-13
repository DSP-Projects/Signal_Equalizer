from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
import sys
import numpy as np
from PyQt5.QtCore import Qt

class MusicMode(Mode):
    
    def __init__(self, sliders_widget, sample_instance, graph2,graph3, graph1,spectrogram_widget2, num_of_sliders: int=4):
            super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2, graph3, spectrogram_widget2, graph1)
            self.old_value=5
            # Guitar  ,  Flute  ,  Harmonica  ,   Xylophone
            self.freq_ranges['piano'] =  [(0,10), (250, 275), (505, 540), (780, 790),(1040, 1060), (1565, 1590), (1840, 1850),(2105, 2120), (2375, 2395), (2650, 2665), (2925, 2940), (3200, 3215), (3487,3491), (3770, 3780), (4345, 4355), (4638, 4656), (4900, 4980)]
            self.freq_ranges['violin'] =  [(1020, 1060), (1520, 1600), (2560, 2640), (3080, 3180), (3590, 3720),(4110,4230),(4640,4650), (5140,5345)]
            self.freq_ranges['triangle'] =  [(4600, 5000), (5170, 5250), (5350, 5550), (5600,22000)]
            self.freq_ranges['xilaphone'] =  [(300,1000)]
            


    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        gain_factor = gain_value/self.old_value # to handle slider values correctly 
        self.old_value= gain_value
        freq_mag_modified=[]
        if(slider_index==0):
                instrument='piano'
        elif(slider_index==1):
                instrument='violin' 
        elif(slider_index==2):
                instrument='triangle'
        elif(slider_index==3):
                instrument='xilaphone'         
        # Get the frequency range for this slider
        freq_range = self.freq_ranges[instrument]

        # Apply gain only to frequencies within the specified range
        freq_mag_modified = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                freq_mag * gain_factor, 
                                freq_mag)
        

        
        # Plot the updated frequency domain
        self.plot_inverse_fourier(freq_mag_modified, freq_phase, self.time, self.graph2)
        self.plot_fourier_domain(freq_list, freq_mag_modified)
     
                   
                   
                
 