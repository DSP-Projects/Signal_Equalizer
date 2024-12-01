from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QSlider,QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
import numpy as np
from Reconstruction import Reconstruction
from Spectrogram import Spectrogram
from PyQt5.QtGui import QPixmap

class Mode(ABC):
    def __init__(self, sliders_widget, num_of_sliders, sample_instance, graph2, graph3, spectrogram_widget2, graph1):
        # Initialize the attributes to avoid AttributeError
        self.sliders_list = []       # List of slider widgets
        self.slider_labels = []      # List of tuples (label, icon label)
        self.clear_sliders(sliders_widget)  # Clear any existing sliders

        # Assign remaining attributes
        self.sliders_widget = sliders_widget
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

            slider.setCursor(Qt.PointingHandCursor)

            # Create a horizontal layout for the label and icon
            label_container = QWidget()
            label_layout = QHBoxLayout(label_container)


            icon_label = QLabel()  # QLabel for the icon
            icon_pixmap = QPixmap()  # Initialize with an empty QPixmap (to be updated later)
            icon_label.setPixmap(icon_pixmap.scaled(20, 20, Qt.KeepAspectRatio))  # Set default size for the icon

            label = QLabel("Default")  # Default text, to be updated based on mode
            label.setAlignment(Qt.AlignCenter)

            # Add icon and label to the horizontal layout
            label_layout.addWidget(icon_label)
            label_layout.addWidget(label)
            label_layout.setAlignment(Qt.AlignCenter)
            label_layout.setContentsMargins(0, 0, 0, 0)

            # Add slider and label to the container's layout
            slider_layout.addWidget(slider)
            slider_layout.addWidget(label_container)  # Use the label container here
            slider_layout.setAlignment(Qt.AlignCenter)

            # Add container to the main layout
            main_layout.addWidget(slider_container)

            # Store references
            self.sliders_list.append(slider)
            self.slider_labels.append((label, icon_label)) 

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
        """
        Clear the sliders widget layout and reset associated attributes.
        """
        layout = sliders_widget.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Clear the references
        self.sliders_list = []
        self.slider_labels = []

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

    def update_slider_labels(self, mode, freq_ranges=None):
        """
        Update the labels under the sliders based on the selected mode.
        :param mode: The mode as a string ('Uniform', 'Instrument', 'Animal', 'ECG').
        """
        labels_map = {
            "Uniform": [f"{int(freq_range[0])}-{int(freq_range[1])}" for freq_range in freq_ranges],
            "Instrument": ["piano", "violin",  "triangle",  "xylophone"],
            "Animal": ["Dogs", "Wolves", "Crow", "Bat"],
            "ECG": ["Normal", "Atrial flutter", "Ventricular tachycardia", "Atrial fibrillation"]
        }

        icons_map = {
            "Instrument": ["icons/piano.png", "icons/violin.png",  "icons/triangle.png",  "icons/xylophone.png"],
            "Animal": ["icons/dog.png", "icons/wolf.png", "icons/crow.png", "icons/bat.png"],
            
        }

        labels = labels_map.get(mode, ["Default"] * len(self.slider_labels))
        icons = icons_map.get(mode, [None] * len(self.slider_labels))

        for (label, icon_label), text, icon_path in zip(self.slider_labels, labels, icons):
                # Update label text
                label.setText(text)
                label.setStyleSheet("font-weight: bold; font-size: 17px; color: #2e556d;")
                label.setStyleSheet("padding-left: 2px;")

                # Update icon
                icon_pixmap = QPixmap(icon_path)
                icon_label.setPixmap(icon_pixmap.scaled(40, 40, Qt.KeepAspectRatio))
                icon_label.setStyleSheet("padding-left: 0px;")
                