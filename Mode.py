from abc import ABC, abstractmethod

class Mode(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def update_sliders(self):
        pass