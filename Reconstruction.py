import numpy as np

class Reconstruction:
    def __init__(self,modified_fft):
        self.modified_fft=modified_fft

    def inverse_fourier(self):
        return np.fft.ifft(self.modified_fft).real