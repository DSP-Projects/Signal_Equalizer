from Mode import Mode
from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtCore import Qt

class UniformMode(Mode):
    
    def __init__(self, sliders_widget, num_of_sliders):
        super().__init__(sliders_widget, num_of_sliders)
        
        
    
    def init_mode(self, freq_list):
        '''
        params:
        freq_list: a list of whole freq components in the signal
       
        '''
        pass

    def update_mode_upon_sliders_change(self, slider_no, new_value):
        '''
        returns:
        list of new freq_componets 
        '''
        pass
