from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import pyqtgraph as pg
import os
from Spectrogram import Spectrogram
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("SignalEqualizer.ui", self)
        self.setWindowTitle("Signal Equalizer")

        self.mode_chosen= self.findChild('QComboBox', "Mode")
        self.mode_chosen.IndexChanged.connect(self.change_mode)
        
        spectrogram_plot = Spectrogram()
        self.layout.addWidget(spectrogram_plot.canvas)
        

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