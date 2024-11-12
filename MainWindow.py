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
from sampling import Sampling
import numpy as npr
from UniformMode import UniformMode
from MusicMode import MusicMode
from ECGAbnormalities_mode import ECGAbnormalities
from AnimalMode import AnimalMode
import simpleaudio as sa
from pydub import AudioSegment


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("SignalEqualizer.ui", self)
        self.setWindowTitle("Signal Equalizer")


        
         #hajar
        # Initialize the scale combo box
        self.scale_combo_box = self.findChild(QComboBox, 'scale')
        self.scale_combo_box.setCurrentIndex(0)  # Set default to "Linear Scale"
        self.scale_combo_box.currentIndexChanged.connect(self.change_scale)
        self.sampling = Sampling()
        self.signal=None 
        self.sample_rate = 1000 
        self.file_path=None
        self.mode_chosen= self.findChild(QComboBox, "mode")
        self.mode_chosen.setCurrentIndex(0)
        self.mode_chosen.currentIndexChanged.connect(self.change_mode)
        self.mode_instance=None
        self.sliders_widget= self.findChild(QWidget, 'slidersWidget') 
        
        self.spectrogram_input = Spectrogram()
        self.spectrogram_output = Spectrogram()


        self.audiobefore = self.findChild(QPushButton, 'audioBefore')
        self.audiobefore.clicked.connect(self.audio_before)
        self.audioafter = self.findChild(QPushButton, 'audioAfter')
        self.audioafter.clicked.connect(self.audio_after)
        self.signal=None
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
        self.rewind = self.findChild(QPushButton, "radioButton")
        self.rewind.clicked.connect(self.rewind_signal)
        self.spectrogram_widget1 = self.findChild(QWidget, 'spectogram1') 
        self.spectrogram_widget2 = self.findChild(QWidget, 'spectogram2') 
        self.spectrogram_check = self.findChild(QCheckBox, 'spectogramCheck')
        self.spectrogram_check.stateChanged.connect(self.handle_checkbox_state)
        self.speed = self.findChild(QSlider, 'speedSlider')
        self.speed.setMinimum(10)  # Set minimum zoom value
        self.speed.setMaximum(200)  # Set maximum zoom value
        self.speed.setValue(150)  # Set initial zoom value
        self.speed.valueChanged.connect(self.set_speed_value) 

        # self.toggle_stat_original_audio = self.findChild(QPushButton, 'audioBefore')
        # self.toggle_stat_original_audio.clicked.connect(self.play_original_audio_func)
      

        self.graph1 = self.findChild(pg.PlotWidget, 'graph1')
        self.graph2 = self.findChild(pg.PlotWidget, 'graph2')
        self.graph3 = self.findChild(pg.PlotWidget, 'graph3')

        self.graph1 = Graph(self.graph1, "Graph 1", "", "")
        self.graph2 = Graph(self.graph2, "Graph 2", "", "")
        self.graph3 = Graph(self.graph3,  "Frequency Domain", "Frequency (Hz)", "Magnitude")
        


        self.load_instance = Load()  # Instance of the Load class

        self.play_icon = QIcon("icons/play.png")
        self.pause_icon = QIcon("icons/pause (2).png")
        self.play.setIcon(self.pause_icon)

        self.audiobefore.setIcon(self.pause_icon)
        self.audioafter.setIcon(self.pause_icon)
        self.current_icon = 1
        self.audiobefore.setText('Pause')
        self.audioafter.setText('Pause')

        #self.change_mode(0)

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
        if self.spectrogram_check.isChecked(): 
            self.spectrogram_widget1.setVisible(False) 
            self.spectrogram_widget2.setVisible(False) 
            print("PlotWidgets are hidden") 
        else: 
            self.spectrogram_widget1.setVisible(True) 
            self.spectrogram_widget2.setVisible(True) 
            print("PlotWidgets are visible")


    def change_scale(self):
        """Update the graph to use either linear or audiogram scale based on combo box selection."""
        selected_scale = self.scale_combo_box.currentText()
       
        if selected_scale == "Audiogram Scale":
            self.sampling.set_scale(True)  # Set to audiogram (logarithmic) scale
            self.mode_instance.set_is_audiogram(True)
            is_audiogram= True
        else:
            self.sampling.set_scale(False)  # Set to linear scale
            is_audiogram= False

        # Re-plot frequency domain with the selected scale
        if self.signal.signal_data_time is not None and self.signal.signal_data_amplitude is not None:
            self.sampling.plot_frequency_domain(self.sampling.get_frequencies(),self.sampling.get_magnitudes(), is_audiogram, self.graph3)        

    # def play_original_audio_func(self):
    #     audio = AudioSegment.from_file(self.file_path)
    #     sample_rate = audio.frame_rate
    #     samples = np.array(audio.get_array_of_samples())
    #     audio_obj = sa.play_buffer(samples.tobytes(), 1, 2, sample_rate)
    #     audio_obj.wait_done() 
    

    def load_signal(self): 
         self.file_path = self.load_instance.browse_signals() 
         self.clear_signals()
         if self.file_path: 
              # Handle the loaded signal 
              # For example, load the signal data into a graph 
              try: 
                  self.prepare_load(self.file_path)
              except Exception as e: 
                QMessageBox.warning(self, "Error", f"Failed to load signal: {e}") 
    def rewind_signal(self):        
        self.graph1.rewind()
        self.graph2.rewind()

    def clear_signals(self): 
        self.graph1.clear_signal() 
        self.graph2.clear_signal() 
        self.graph3.clear_signal() 

    def audio_before(self):
        if self.current_icon == 1: 
            self.audiobefore.setIcon(self.play_icon)
            self.audiobefore.setText("Play")
            self.current_icon = 2
        else: 
            self.audiobefore.setIcon(self.pause_icon) 
            self.audiobefore.setText("Pause")   
            self.current_icon = 1 

    def audio_after(self):  
        if self.current_icon == 1: 
            self.audioafter.setIcon(self.play_icon)
            self.audioafter.setText("Play")

            self.current_icon = 2 
        else:
            self.audioafter.setIcon(self.pause_icon) 
            self.audioafter.setText("Pause")
            self.current_icon = 1    
    

    def toggle_play_pause(self): 
        self.graph1.toggle_play_pause() 
        self.graph2.toggle_play_pause() 
        if self.graph1.is_paused: 
            self.play.setIcon(self.play_icon) 
        else: 
            self.play.setIcon(self.pause_icon)
    
    def change_mode(self, index):
        print(index)
        match index:
            case 0: #uniform
                    self.mode_instance= UniformMode(self.sliders_widget, self.sampling, self.graph2, self.graph3, self.graph1, self.spectrogram_widget2)     
            case 1: #musical 
                    self.mode_instance= MusicMode(self.sliders_widget, self.sampling, self.graph2, self.graph3,self.graph1, self.spectrogram_widget2)
            case 2: #animal
                    self.mode_instance= AnimalMode(self.sliders_widget, self.sampling,self.graph2, self.graph3,self.graph1, self.spectrogram_widget2)
            case 4: #ECG
                    self.mode_instance= ECGAbnormalities(self.sliders_widget, self.sampling, self.graph2, self.graph3, self.graph1, self.spectrogram_widget2)
    
    def set_default(self):
        file_path="output4.csv"
        self.change_mode(0)
        self.prepare_load(file_path)
           
    def prepare_load(self, file_path):
        self.signal=Signal(3,file_path) 
        self.sampling.update_sampling(self.graph3, self.signal.signal_data_time, self.signal.signal_data_amplitude,self.sample_rate)
        print(self.signal.signal_data_amplitude)
        if(self.signal.signal_data_amplitude is not None and len(self.signal.signal_data_amplitude) > 0 ):           
            self.sampling.compute_fft(self.signal.signal_data_time,self.signal.signal_data_amplitude)
            self.sampling.plot_frequency_domain(self.sampling.get_frequencies(),self.sampling.get_magnitudes(), False, self.graph3)
        self.signal=Signal(1,file_path)
        self.spectrogram_input.plot_spectrogram(self.signal.signal_data_amplitude, self.sample_rate, self.spectrogram_widget1)
        self.spectrogram_output.plot_spectrogram(self.signal.signal_data_amplitude, self.sample_rate, self.spectrogram_widget2)
        self.mode_instance.set_time(self.signal.signal_data_time)
        self.graph1.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude) 
        self.graph2.set_signal(self.signal.signal_data_time, self.signal.signal_data_amplitude)      
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.set_default()
    sys.exit(app.exec_())