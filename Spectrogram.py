from scipy.signal import spectrogram
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout

class Spectrogram:
    def __init__(self):
        fig = Figure()
        self.canvas= FigureCanvas(fig)
        self.canvas.axes = fig.add_subplot(111) 


    def plot_spectrogram(self, data, sampling_freq, spectrogram_widget):
        """
        data: time series signal values
        """
        f, t, Sxx = spectrogram(data, sampling_freq)  #returns sample frequencies, time samples, spectrogram  of data
        Sxx_dB = 10 * np.log10(Sxx)
        self.canvas.axes.clear()
        img = self.canvas.axes.imshow(Sxx_dB, aspect='auto', origin='lower',
                                            extent=[t.min(), t.max(), f.min(), f.max()],
                                            cmap='viridis')
        
        self.canvas.axes.set_xlabel("Time [s]")
        self.canvas.axes.set_ylabel("Frequency [Hz]")
        self.canvas.axes.set_title("Spectrogram")
        
        self.canvas.figure.colorbar(img, ax=self.canvas.axes, label='Intensity [dB]')
        
        self.canvas.draw()

        if spectrogram_widget.layout() is None:
            layout = QVBoxLayout(spectrogram_widget)
            spectrogram_widget.setLayout(layout)
        else:
            layout = spectrogram_widget.layout()

        # Add the canvas to the parent's layout
        layout.addWidget(self.canvas)


    def hide_spectrogram(self):
        self.canvas.hide()
    
    def show_spectrogram(self):
        self.canvas.show()