import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget

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
        self.graphWidget.setBackground('#0c202a')
    

        # Configure plot labels and axis colors
        self.graphWidget.getAxis('left').setPen(pg.mkPen(color='w', width=2))
        self.graphWidget.getAxis('bottom').setPen(pg.mkPen(color='w', width=2))
        self.graphWidget.getAxis('left').setTextPen(pg.mkPen(color='w'))
        self.graphWidget.getAxis('bottom').setTextPen(pg.mkPen(color='w'))

        
        # Label axes with color and size
        self.graphWidget.setLabel('left', ylabel, **{'color': '#ffffff', 'font-size': '10pt'})
        self.graphWidget.setLabel('bottom', xlabel, **{'color': '#ffffff', 'font-size': '10pt'}) 
        #self.graphWidget.setXRange(1, 20, padding=0)


        
        self.signal_plot = self.graphWidget.plot()

        self.signal_x = []
        self.signal_y = []

    def set_signal(self, signal_x, signal_y):
        self.clear_signal()
        self.signal_x = signal_x
        self.signal_y = signal_y
        self.graphWidget.plot(self.signal_x, self.signal_y, pen='#3286ad')

    def clear_signal(self):
        self.graphWidget.clear()
        self.signal_x = []
        self.signal_y = []
