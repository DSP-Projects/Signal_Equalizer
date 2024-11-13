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


        self.modified_frequencies = None
        self.modified_magnitudes = None
        self.modified_phases = None

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
    
    def compute_fft(self, signal_data_time, signal_data_amplitude):

        fft_result = np.fft.fft(signal_data_amplitude)
        frequencies = np.fft.fftfreq(len(fft_result), (signal_data_time[1] - signal_data_time[0]))
        
        magnitudes = np.abs(fft_result)
        phases = np.angle(fft_result)
         

        positive_frequencies = frequencies > 0

        self.frequencies=frequencies[positive_frequencies]
        self.magnitudes=magnitudes[positive_frequencies]
        self.phases= phases[positive_frequencies]

    def plot_frequency_domain(self, frequencies, magnitudes, is_audiogram_scale, graph):
        """Plot frequency domain with support for audiogram scale."""
        graph.clear_signal()
        audiogram_freqs = np.array([125, 250, 500, 1000, 2000, 4000, 8000])  # Standard audiogram frequencies
        min_db = -60  # Minimum dB level to display
        ref_level = 1.0  # Reference level for dB calculation

        if is_audiogram_scale:
            # Interpolate the magnitudes at audiogram frequencies
            audiogram_magnitudes = np.interp(audiogram_freqs, self.frequencies, 20 * np.log10(self.magnitudes / ref_level + 1e-10))
            audiogram_magnitudes = np.maximum(audiogram_magnitudes, min_db)  # Ensure a minimum dB level

            # Plot audiogram with markers
            audiogram_plot = pg.PlotDataItem(
                audiogram_freqs,
                audiogram_magnitudes,
                pen=pg.mkPen('b', width=2),
                symbol='o',
                symbolSize=10
            )
            graph.graphWidget.addItem(audiogram_plot)
            graph.graphWidget.setLogMode(x=True, y=False)
            graph.graphWidget.setXRange(np.log10(100), np.log10(10000))  # Logarithmic scale range
            graph.graphWidget.setYRange(min_db, 20)

            # Set custom ticks for the audiogram frequencies
            tick_values = [(np.log10(freq), str(freq)) for freq in audiogram_freqs]
            graph.graphWidget.getAxis('bottom').setTicks([tick_values])
            graph.graphWidget.getAxis('bottom').setLabel('Frequency (Hz)', units='Hz')
        else:
            # Standard linear plot
            linear_plot = pg.PlotDataItem(
                frequencies,
                magnitudes,
                pen=pg.mkPen('b', width=2)
            )
            graph.graphWidget.addItem(linear_plot)
            graph.graphWidget.setLogMode(x=False, y=False)
            graph.graphWidget.setXRange(0,frequencies[-1])  # Adjust for musical mode or lower frequency ranges
            graph.graphWidget.setYRange(0, np.max(self.magnitudes))

            # Set custom ticks for the linear frequencies
            tick_values = [(freq, str(freq)) for freq in np.linspace(0, 2000, num=11)]
            graph.graphWidget.getAxis('bottom').setTicks([tick_values])
            graph.graphWidget.getAxis('bottom').setLabel('Frequency (Hz)', units='Hz')

    def get_frequencies(self):
        return self.frequencies

    def get_magnitudes(self):
        return self.magnitudes

    def get_phases(self):
        return self.phases

    