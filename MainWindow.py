from PyQt5.QtWidgets import QMainWindow ,QMessageBox, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import os
from Spectrogram import Spectrogram
from Graph import Graph
from PyQt5.QtGui import QIcon
from Load import Load
from Signal import Signal
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("SignalEqualizerr.ui", self)
        self.setWindowTitle("Signal Equalizer")

    #     self.mode_chosen= self.findChild('QComboBox', "Mode")
    #     self.mode_chosen.IndexChanged.connect(self.change_mode)
        
    #     spectrogram_plot = Spectrogram()
    #     self.layout.addWidget(spectrogram_plot.canvas)



        self.zoom_in_button = self.findChild(QPushButton, 'zoomIn') 
        self.zoom_in_button.clicked.connect(self.zoom_in) 
        self.zoom_out_button = self.findChild(QPushButton, 'zoomOut') 
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.browsefile = self.findChild(QPushButton, 'browseFile')
        self.browsefile.clicked.connect(self.load_signal)
        self.play = self.findChild(QPushButton, 'play')
        self.play.clicked.connect(self.toggle_play_pause)
        self.removefile = self.findChild(QPushButton, 'removeFile')
        self.removefile.clicked.connect(self.clear_signals)
        self.rewind = self.findChild(QRadioButton, "radioButton")
        self.rewind.clicked.connect(self.rewind_signal)
        self.graph4 = self.findChild(PlotWidget, 'widget') 
        self.graph5 = self.findChild(PlotWidget, 'spectogram2') 
        self.checkbox = self.findChild(QCheckBox, 'spectogramCheck')
        self.checkbox.stateChanged.connect(self.handle_checkbox_state)
        self.speed = self.findChild(QSlider, 'speedSlider')
        self.speed.setMinimum(1)  # Set minimum zoom value
        self.speed.setMaximum(200)  # Set maximum zoom value
        self.speed.setValue(100)  # Set initial zoom value
        self.speed.valueChanged.connect(self.set_speed_value) 

      

        self.graph1 = self.findChild(pg.PlotWidget, 'graph1')
        self.graph2 = self.findChild(pg.PlotWidget, 'graph2')
        self.graph3 = self.findChild(pg.PlotWidget, 'graph3')

        self.graph1 = Graph(self.graph1, "Graph 1", "", "")
        self.graph2 = Graph(self.graph2, "Graph 2", "", "")
        self.graph3 = Graph(self.graph3, "Graph 3", "", "")
        self.graph4_instance = Graph(self.graph4, "Graph 4", "", "")
        self.graph5_instance = Graph(self.graph5, "Graph 5", "", "")
        




        self.load_instance = Load()  # Instance of the Load class

        self.play_icon = QIcon("icons/play.png")
        self.pause_icon = QIcon("icons/pause (2).png")
        self.play.setIcon(self.pause_icon)


    def set_speed_value(self, value): 
        self.graph1.set_speed(value) 
        self.graph2.set_speed(value)


    def zoom_in(self):
        self.graph1.zoom_in() 
        self.graph2.zoom_in()

    def zoom_out(self):
        self.graph1.zoom_out() 
        self.graph2.zoom_out()  


    def handle_checkbox_state(self): 
        if self.checkbox.isChecked(): 
            self.graph4.setVisible(False) 
            self.graph5.setVisible(False) 
            print("PlotWidgets are hidden") 
        else: 
            self.graph4.setVisible(True) 
            self.graph5.setVisible(True) 
            print("PlotWidgets are visible")

    def load_signal(self): 
         file_path = self.load_instance.browse_signals() 
         if file_path: 
              # Handle the loaded signal 
              # For example, load the signal data into a graph 
              try: 
                  signal_data = np.loadtxt(file_path, delimiter=',', skiprows=1) 
                  self.graph1.set_signal(signal_data[:, 0], signal_data[:, 1]) 
              except Exception as e: 
                  QMessageBox.warning(self, "Error", f"Failed to load signal: {e}") 

    def rewind_signal(self):        
        pass

    def clear_signals(self): 
        self.graph1.clear_signal() 
        self.graph2.clear_signal() 
        self.graph3.clear_signal() 
    

    def toggle_play_pause(self): 
        self.graph1.toggle_play_pause() 
        self.graph2.toggle_play_pause() 
        self.graph3.toggle_play_pause() 
        if self.graph1.is_paused: 
            self.play.setIcon(self.play_icon) 
        else: 
            self.play.setIcon(self.pause_icon)
    
    def change_mode(self, index):
        match index:

            case 0: #uniform
                #instatantiate object from uniform mode class and apply changes onto it
                pass
            case 1: #musical 
                pass
            case 2: #animal
                pass
            case 4: #ECG
                pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())