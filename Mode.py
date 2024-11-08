from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtCore import Qt

class Mode(ABC):
    def __init__(self, sliders_widget, num_of_sliders):
        self.freq_ranges= None
        self.sliders_widget=sliders_widget
        self.sliders_list=[]
        self.gain_limits = (0, 10)

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

        layout.setSpacing(10)

    @abstractmethod
    def init_mode(self, freq_list):
        '''
        give each slider the range corresponding to it
        params:
        freq_list: a list of whole freq components in the signal
       
        '''
        pass
    
    @abstractmethod
    def update_mode_upon_sliders_change(self, slider_no, new_value):
        '''
        returns:
        list of new freq_componets 
        '''
        pass
