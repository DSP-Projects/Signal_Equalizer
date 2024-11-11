from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
import math 
from Reconstruction import Reconstruction

class Mode(ABC):
    def __init__(self, sliders_widget, num_of_sliders, sample_instance, graph2, graph3):
        self.freq_ranges= None
        self.sliders_widget=sliders_widget
        self.sliders_list=[]
        self.gain_limits = (0, 10)
        self.sample= sample_instance
        self.time= None
        self.graph2= graph2
        self.graph3= graph3
        self.is_audiogram= False
        
      
        if self.sliders_widget.layout() is None:
            layout = QVBoxLayout(self.sliders_widget)
            self.sliders_widget.setLayout(layout)
        else:
            layout = self.sliders_widget.layout()
        for _ in range(num_of_sliders):
            slider = QSlider(Qt.Vertical) 
            slider.setRange(self.gain_limits[0], self.gain_limits[1])  # Set slider range to control gain
            slider.setValue(5)
            layout.addWidget(slider)
            self.sliders_list.append(slider)
        
        for idx, slider in enumerate(self.sliders_list):
            slider.valueChanged.connect(lambda value, idx=idx: self.update_mode_upon_sliders_change(idx, value, self.sample.freq_list, self.sample.freq_mag, self.sample.freq_phase))

        layout.setSpacing(30)



    @abstractmethod
    def update_mode_upon_sliders_change(self, slider_no, new_value, freq_list, freq_mag, freq_phase):
        '''
        returns:
        list of new freq_componets 
        '''
        pass

    def send_reconstruct(self, freq_mag, freq_phase):
            signal = []
            for mag, phase in zip(freq_mag, freq_phase):
                x = mag * math.cos(phase)
                y = mag * math.sin(phase)
                signal.append(complex(x, y))
            return signal

    def plot_inverse_fourier(self, freq_mag, freq_phase, time, graph):
        signal = self.send_reconstruct(freq_mag, freq_phase)
        self.reconstruct= Reconstruction(signal)
        self.reconstruct.inverse_fourier(time,graph)

    def plot_fourier_domain(self, freq_list, freq_mag):
        self.sample.plot_frequency_domain( freq_list, freq_mag, is_audiogram= self.is_audiogram, graph3= self.graph3)

    def set_time(self, time):
        self.time = time

    def set_is_audiogram(self, is_audiogram):
        self.is_audiogram= is_audiogram
