from abc import ABC, abstractmethod

class Mode(ABC):
    def __init__(self):
        self.freq_ranges= None


    @abstractmethod
    def update_sliders(self):
        pass 