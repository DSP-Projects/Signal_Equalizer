import sys
import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph as pg
from sampling import Sampling

class TestSamplingApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the SamplingClass
        self.sampling = Sampling()

        # Set up the main window layout
        self.setWindowTitle("Fourier Transform with Scale Toggle")
        self.setGeometry(100, 100, 800, 600)
        
        # Create the graph widget
        self.graphWidget = pg.PlotWidget(title="Frequency Domain")
        self.setCentralWidget(self.graphWidget)

        # Create a button to toggle between linear and audiogram scales
        self.toggleButton = QtWidgets.QPushButton("Toggle Audiogram Scale")
        self.toggleButton.clicked.connect(self.toggle_scale)

        # Create layout for controls
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.toggleButton)

        # Set up central widget and layout
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Example test data: sine wave with noise
        self.signal_time = np.linspace(0, 1, 500)
        self.signal_amplitude = np.sin(2 * np.pi * 50 * self.signal_time) + 0.5 * np.random.normal(size=500)
        self.sample_rate = 1000  # in Hz

        # Plot the initial Fourier transform
        self.update_plot()

    def toggle_scale(self):
        """Toggle the scale and update the plot."""
        self.sampling.set_scale(not self.sampling.is_audiogram_scale)
        self.update_plot()

    def update_plot(self):
        """Update the Fourier transform plot based on the current scale setting."""
        self.sampling.plot_frequency_domain(self, self.signal_time, self.signal_amplitude)

    def clear_signal(self):
        """Clear existing plots from the graph widget."""
        self.graphWidget.clear()

# Run the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testApp = TestSamplingApp()
    testApp.show()
    sys.exit(app.exec_())
