import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class Sampling:
    def __init__(self):
        super().__init__()
        self.sampled_time = None
        self.sampled_data = None
        self.sampling_interval = None
        
        self.is_audiogram_scale = False  # Start with linear scale by default
        
        # Variables to store frequency, magnitude, and phase
        self.frequencies = None
        self.magnitudes = None
        self.phases = None

    def sample_signal(self, signal_data_time, signal_data_amplitude, sample_rate):
        self.sampling_interval = 1 / sample_rate
        self.sampled_time = np.arange(0, max(signal_data_time), self.sampling_interval)
        self.sampled_data = np.interp(self.sampled_time, signal_data_time, signal_data_amplitude)
        return self.sampled_time, self.sampled_data

    def update_sampling(self, graph, signal_data_time, signal_data_amplitude, sample_rate):
        self.sampled_time, self.sampled_data = self.sample_signal(signal_data_time, signal_data_amplitude, sample_rate)

    def set_scale(self, audiogram_scale):
        """Toggle the frequency scale between linear and audiogram."""
        self.is_audiogram_scale = audiogram_scale

    def plot_frequency_domain(self, graph, signal_data_time, signal_data_amplitude):
        if signal_data_amplitude is not None:
            fft_result = np.fft.fft(signal_data_amplitude)
            frequencies = np.fft.fftfreq(len(fft_result), (signal_data_time[1] - signal_data_time[0]))
            magnitudes = np.abs(fft_result)
            self.phases = np.angle(fft_result)
            positive_frequencies = frequencies > 0
            self.frequencies = frequencies[positive_frequencies]
            self.magnitudes = magnitudes[positive_frequencies]
            graph.clear_signal()

            if self.is_audiogram_scale:
                
                # Plot using logarithmic scale for magnitudes
                log_magnitude = 20 * np.log10(self.magnitudes+ 1e-10)  # Avoid log(0)
                plot_data = ( self.frequencies, log_magnitude)
            else:
                # Use linear scale
                plot_data = (self.frequencies, self.magnitudes)

            original_plot = pg.PlotDataItem(
                plot_data[0],  # frequencies
                plot_data[1],  # magnitudes
                pen=pg.mkPen('b', width=2)
            )
            graph.graphWidget.addItem(original_plot)

    def get_frequencies(self):
        """Return the frequencies array."""
        return self.frequencies

    def get_magnitudes(self):
        """Return the magnitudes array."""
        return self.magnitudes

    def get_phases(self):
        """Return the phases array."""
        return self.phases

    