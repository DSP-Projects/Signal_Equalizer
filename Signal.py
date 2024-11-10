import pandas as pd
from scipy.io import wavfile
import numpy as np
class Signal:
    def __init__(self, graph_num,file_path):
        self.file_extension = self.file_path.split('.')[-1].lower()
        self.signal_data_amplitude=None
        self.signal_data_time=None


        if(self.file_extension=="csv"):
            self.csv_path = file_path
            csvFile = pd.read_csv(self.csv_path)   
            self.signal_data_time = csvFile.iloc[:3000, 0].values
            self.signal_data_amplitude = csvFile.iloc[:3000, 1].values
            self.graph_num= graph_num
        elif(self.file_extension=="wav"):
            sample_rate, signal = wavfile.read(file_path)
            # Convert sample indices to time (in seconds)
            duration = len(signal) / sample_rate  # Total duration in seconds
            self.signal_data_time = np.linspace(0, duration, len(signal)) 
            self.signal_data_amplitude=signal

    def set_signal_graph_num(self, new_graph_num):
        self.graph_num = new_graph_num

    def get_signal_graph_num(self):
        return self.graph_num    

        
