from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
import numpy as np
from Reconstruction import Reconstruction
from Spectrogram import Spectrogram

class Mode(ABC):
    def __init__(self, sliders_widget, num_of_sliders, sample_instance, graph2, graph3, spectrogram_widget2, graph1):
        self.clear_sliders(sliders_widget)

        self.sliders_widget = sliders_widget
        self.sliders_list = []
        self.slider_labels = []
        self.gain_limits = (0, 10)
        self.sample = sample_instance
        self.time = None
        self.sample_rate = None
        self.graph2 = graph2
        self.graph3 = graph3
        self.is_audiogram = False
        self.graph1 = graph1
        self.spectrogram_widget2 = spectrogram_widget2
        self.spectrogram2 = Spectrogram()
        self.reconstruct = None

        # Set up main layout for the sliders widget
        if self.sliders_widget.layout() is None:
            main_layout = QVBoxLayout(self.sliders_widget)
            self.sliders_widget.setLayout(main_layout)
        else:
            main_layout = self.sliders_widget.layout()

        # Add sliders and their labels
        for _ in range(num_of_sliders):
            # Create a container widget for the slider-label pair
            slider_container = QWidget()
            slider_layout = QVBoxLayout(slider_container)

            slider = QSlider(Qt.Vertical)
            slider.setRange(self.gain_limits[0], self.gain_limits[1])  # Set slider range to control gain
            slider.setValue(5)

            label = QLabel("Default")  # Default text, to be updated based on mode
            label.setAlignment(Qt.AlignCenter)

            # Add slider and label to the container's layout
            slider_layout.addWidget(slider)
            slider_layout.addWidget(label)
            slider_layout.setAlignment(Qt.AlignCenter)

            # Add container to the main layout
            main_layout.addWidget(slider_container)

            # Store references
            self.sliders_list.append(slider)
            self.slider_labels.append(label)

        main_layout.setSpacing(30)

        # Connect sliders to the update function
        for idx, slider in enumerate(self.sliders_list):
            slider.valueChanged.connect(lambda value, idx=idx: self.update_mode_upon_sliders_change(
                idx, value, self.sample.frequencies, self.sample.magnitudes, self.sample.phases
            ))

    @abstractmethod
    def update_mode_upon_sliders_change(self, slider_no, new_value, freq_list, freq_mag, freq_phase):
        """
        Update behavior when sliders change.
        """
        pass

    def send_reconstruct(self, freq_mag, freq_phase):
        signal = freq_mag * np.exp(1j * freq_phase)
        return signal

    def plot_inverse_fourier(self, freq_mag, freq_phase, time, graph):
        signal = self.send_reconstruct(freq_mag, freq_phase)
        self.reconstruct = Reconstruction(signal)
        new_mag = self.reconstruct.inverse_fourier(time, graph)
        self.spectrogram2.plot_spectrogram(new_mag, self.sample_rate, self.spectrogram_widget2)
        # self.graph1.rewind()

    def plot_fourier_domain(self, freq_list, freq_mag):
        self.sample.plot_frequency_domain(freq_list, freq_mag, self.is_audiogram, self.graph3)

    def set_time(self, time):
        self.time = time

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    def set_is_audiogram(self, is_audiogram):
        self.is_audiogram = is_audiogram

    def clear_sliders(self, sliders_widget):
        layout = sliders_widget.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def get_inverse(self):
        if self.reconstruct is not None:
            return self.reconstruct.inverse_fourier(self.time, self.graph2)
        else:
            return None

    def reset_sliders_to_default(self):
        default_value = 5  # Set this to the initial default value of the sliders
        for slider in self.sliders_list:
            slider.setValue(default_value)

    def set_sample_instance(self, sample_instance):
        self.sample = sample_instance

    def update_slider_labels(self, mode):
        """
        Update the labels under the sliders based on the selected mode.
        :param mode: The mode as a string ('Uniform', 'Instrument', 'Animal', 'ECG').
        """
        labels_map = {
            "Uniform": ["10HZ", "20HZ", "30HZ", "40HZ", "50HZ", "60HZ", "70HZ", "80HZ", "90HZ", "100HZ"],
            "Instrument": ["piano", "violin",  "triangle",  "xilaphone"],
            "Animal": ["Dogs", "Wolves", "Crow", "Bat"],
            "ECG": ["Normal", "Atrial flutter", "Ventricular tachycardia", "Atrial fibrillation"]
        }

        labels = labels_map.get(mode, ["Default"] * len(self.slider_labels))
        for label, text in zip(self.slider_labels, labels):
            label.setText(text)
