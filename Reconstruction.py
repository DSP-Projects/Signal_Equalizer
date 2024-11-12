import numpy as np

class Reconstruction:
    def __init__(self,modified_fft):
        self.modified_fft=modified_fft

    def inverse_fourier(self, time, graph):
        new_mag= np.fft.ifft(self.modified_fft).real
        print(new_mag)
        graph.set_signal(time, new_mag)
        return new_mag

