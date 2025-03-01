import numpy as np

class Reconstruction:
    def __init__(self,modified_fft):
        self.modified_fft=modified_fft
        
    def inverse_fourier(self, time, graph):
        new_mag= np.fft.irfft(self.modified_fft)
        #assert len(time) == len(new_mag), "Time and reconstructed signal length mismatch!"
        graph.set_signal(time, new_mag, graph.current_frame)
        return new_mag

