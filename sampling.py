import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class Sampling:
    def __init__(self):
        super().__init__()
        self.sampled_time = None
        self.sampled_data = None
        self.sampling_interval = None
        self.sample_rate=None
        
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
        """
        Compute the real FFT of the input signal and extract frequencies, magnitudes, and phases.
        """
        # Compute rFFT result (real-valued input)
        fft_result = np.fft.rfft(signal_data_amplitude)

        # Compute corresponding positive frequencies
        frequencies = np.fft.rfftfreq(len(signal_data_amplitude), d=(signal_data_time[1] - signal_data_time[0]))
        
        # Compute magnitudes and phases
        magnitudes = np.abs(fft_result)
        phases = np.angle(fft_result)
        
        # Assign the computed components
        self.frequencies = frequencies
        self.magnitudes = magnitudes
        self.phases = phases

        # Debugging output
        print(f"len(self.frequencies): {len(self.frequencies)}")
        print(f"len(self.magnitudes): {len(self.magnitudes)}")



    def plot_frequency_domain(self, frequencies, magnitudes, is_audiogram_scale, graph):
     """Plot frequency domain with support for audiogram scale."""
     graph.clear_signal()  # Clear previous plots

     # Constants
     min_db = -60  # Minimum dB level
     ref_level = 1.0  # Reference level for dB calculation
     epsilon = 1e-10  # Small value to avoid log10(0)
     magnitudes = np.array(magnitudes)

     if is_audiogram_scale:
        # Convert magnitudes to dB
        magnitudes_db = 20 * np.log10(magnitudes / ref_level + epsilon)
        

        valid_indices = frequencies > 0
        frequencies = frequencies[valid_indices]
        magnitudes_db = magnitudes_db[valid_indices]
        frequencies_log = np.log10(frequencies)

        # Plot the audiogram
        audiogram_plot = pg.PlotDataItem(
            frequencies_log,
            magnitudes_db,
            pen=pg.mkPen('b', width=2)  # Blue line
        )
        graph.graphWidget.addItem(audiogram_plot)

        # Set X and Y ranges
        graph.graphWidget.setXRange(np.min(frequencies_log), np.max(frequencies_log))
        graph.graphWidget.setYRange(min_db, np.max(magnitudes_db))

        # Customize X-axis
        x_axis = graph.graphWidget.getAxis('bottom')

        # Generate custom ticks and labels
        tick_positions = np.geomspace(np.min(frequencies), np.max(frequencies), num=30)  
        tick_labels = [
            f"{tick:.1f}" if tick < 1 else f"{int(tick)}"
            for tick in tick_positions
        ]
        ticks = [(np.log10(pos), label) for pos, label in zip(tick_positions, tick_labels)]

        # Show every second tick to alternate labels
        spaced_ticks = [(tick, label) for i, (tick, label) in enumerate(ticks) if i % 1 == 0]
        x_axis.setTicks([spaced_ticks])
        x_axis.setLabel('Frequency (Hz)')
        graph.graphWidget.getAxis('left').setLabel('Intenisty ', units='dB')


     else:
            # Standard linear plot
            linear_plot = pg.PlotDataItem(
                frequencies,
                magnitudes,
                pen=pg.mkPen('b', width=2)
            )
            graph.graphWidget.addItem(linear_plot)
            graph.graphWidget.setLogMode(x=False, y=False)
            graph.graphWidget.setYRange(0, np.max(magnitudes))
            graph.graphWidget.setXRange(np.min(frequencies), np.max(frequencies))



            # Set custom ticks for the linear frequencies
            num_ticks = 15  # Number of ticks you want
            tick_values = np.linspace(0, np.max(frequencies), num_ticks)
            x_tick_labels = [(int(tick), str(int(tick))) for tick in tick_values] 
            graph.graphWidget.getAxis('bottom').setTicks([x_tick_labels])
            graph.graphWidget.getAxis('bottom').setLabel('Frequency (Hz)')
            graph.graphWidget.getAxis('left').setLabel('Amplitude ', units='v')
            
   
    
    def get_frequencies(self):
        return self.frequencies

    def get_magnitudes(self):
        return self.magnitudes

    def get_phases(self):
        return self.phases

    