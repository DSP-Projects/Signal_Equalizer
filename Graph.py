import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout

class Graph:
    def __init__(self, graphWidget, title, xlabel, ylabel):
        self.title = title
        self.graphWidget = graphWidget
        

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
        self.timer.start(100)  # Update the plot every 100 ms

        self.is_paused = False  # To track play/pause state
        self.is_rewinding = False  # To track rewind state

        # Disable panning
        self.graphWidget.getViewBox().setMouseEnabled(x=False, y=False)


    def set_speed(self, interval): 
        self.timer.setInterval(interval)  

    def set_signal(self, signal_x, signal_y):
        self.current_frame = 0  # Reset frame counter when new signal is set
        self.signal_x = signal_x
        self.signal_y = signal_y
        self.update_plot()

    def update_plot(self):
        if not self.is_paused:            
                if self.current_frame < len(self.signal_x):
                    self.current_frame += 1  # Increment frame for normal playback

            # Update the plot with the current frame data
                self.signal_plot.setData(self.signal_x[:self.current_frame], self.signal_y[:self.current_frame], pen=pg.mkPen('#3286ad', width=2))

    def toggle_play_pause(self): 
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(100)

    def toggle_rewind(self):
        pass

    def clear_signal(self):
        self.graphWidget.clear()
        self.signal_x = []
        self.signal_y = []
        self.current_frame = 0
        self.signal_plot = self.graphWidget.plot()  # Recreate the plot item to fully reset

    # def zoom_in(self):
    #     self.graphWidget.getViewBox().scaleBy((0.9, 0.9))

    # def zoom_out(self):
    #     self.graphWidget.getViewBox().scaleBy((1.1,1.1))    