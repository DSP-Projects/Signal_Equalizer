import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout


class Graph:
    def __init__(self, graphWidget, title, xlabel, ylabel, window_size=100, sampling_rate=40):
        """
        Args:
            graphWidget: The PyQtGraph plot widget.
            title (str): Title of the graph.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            window_size (int): Number of samples in one second of data.
            sampling_rate (int): Sampling rate of the data in Hz (samples per second).
        """
        self.title = title
        self.graphWidget = graphWidget
        self.window_size = window_size  # Number of samples for one second
        self.sampling_rate = sampling_rate

        # Ensure the parent widget has a layout
        if graphWidget.layout() is None:
            layout = QVBoxLayout(graphWidget)
            graphWidget.setLayout(layout)
        else:
            layout = graphWidget.layout()
        layout.addWidget(self.graphWidget)

        # Set background and grid
        self.graphWidget.setBackground('#e6eaf1')
        self.graphWidget.setStyleSheet(""" background-color: #e6eaf1;
                                           border-radius: 15px; 
                                           border: 2px solid #ffffff;
                                           box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);""")

        # Configure plot labels and axis colors
        self.graphWidget.getAxis('left').setPen(pg.mkPen(color='#2e556d', width=2))
        self.graphWidget.getAxis('bottom').setPen(pg.mkPen(color='#2e556d', width=2))
        self.graphWidget.getAxis('left').setTextPen(pg.mkPen(color='#2e556d'))
        self.graphWidget.getAxis('bottom').setTextPen(pg.mkPen(color='#2e556d'))

        # Label axes
        self.graphWidget.setLabel('left', ylabel, **{'color': '#2e556d', 'font-size': '10pt'})
        self.graphWidget.setLabel('bottom', xlabel, **{'color': '#2e556d', 'font-size': '10pt'})

        self.signal_plot = self.graphWidget.plot()

        self.signal_x = []
        self.signal_y = []
        self.current_frame = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000 // self.sampling_rate)  # Update at the sampling rate

        self.is_paused = False  # To track play/pause state
        self.is_user_panning = False  # To track if the user is panning manually
        self.phase = 1  # Phase 1: Initial window, Phase 2: Sliding window

        # Connect panning detection
        self.graphWidget.scene().sigMouseClicked.connect(self.resume_sliding_window)

    def set_speed(self, interval):
        self.timer.setInterval(int(interval))  # Ensure the interval is an integer


    def set_signal(self, signal_x, signal_y, current_frame=0):
        """Set the signal data to display."""
        self.current_frame = current_frame  # Reset frame counter when new signal is set
        self.signal_x = signal_x
        self.signal_y = signal_y
        self.update_plot()

    def update_plot(self):
        """Update the plot with data while keeping all data available for panning."""
        if not self.is_paused and not self.is_user_panning:
            if self.current_frame < len(self.signal_x):  # Ensure we don't exceed data limits
                # Always plot all data up to the current frame
                self.signal_plot.setData(
                    self.signal_x[:self.current_frame],  # Show all data up to current frame
                    self.signal_y[:self.current_frame],
                    pen=pg.mkPen('#3286ad', width=2)
                )

                # Set the sliding window for the current visible range
                if self.current_frame >= self.window_size:
                    # Shift the visible range to match the sliding window
                    self.graphWidget.setXRange(
                        self.signal_x[self.current_frame - self.window_size],  # Start of window
                        self.signal_x[self.current_frame],  # End of window
                        padding=0
                    )

                # Increment the current frame
                self.current_frame += 1
            else:
                # Stop the timer when data ends
                self.timer.stop()


    def toggle_play_pause(self):
        """Toggle between play and pause states."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start()

    def resume_sliding_window(self, event):
        """Detect if the user clicked to stop panning and reset sliding."""
        self.is_user_panning = False
        if not self.is_paused and self.current_frame >= self.window_size:
            self.graphWidget.setXRange(
                self.signal_x[self.current_frame - self.window_size],
                self.signal_x[self.current_frame],
                padding=0
            )

    def rewind(self):
        """Rewind the graph to the start."""
        self.current_frame = 0
        self.phase = 1  # Reset to initial window phase
        self.update_plot()

    def zoom_in(self):
        """Zoom into the graph."""
        self.graphWidget.getViewBox().scaleBy((0.9, 0.9))

    def zoom_out(self):
        """Zoom out of the graph."""
        self.graphWidget.getViewBox().scaleBy((1.1, 1.1))

    def clear_signal(self):
        """Clear the graph data."""
        self.graphWidget.clear()
        self.signal_x = []
        self.signal_y = []
        self.current_frame = 0
        self.signal_plot = self.graphWidget.plot()  # Recreate the plot item to fully reset
