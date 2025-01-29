import pandas as pd
from scipy.io import wavfile
import numpy as np
class Signal:
    def __init__(self, graph_num,file_path):
        self.file_extension = file_path.split('.')[-1].lower()
        self.signal_data_amplitude=None
        self.signal_data_time=None
        self.sample_rate=None
        self.signalnoisy=None

        if(self.file_extension=="csv"):
            self.csv_path = file_path
            csvFile = pd.read_csv(self.csv_path)   
            self.signal_data_time = csvFile.iloc[:3000, 0].values
            self.signal_data_amplitude = csvFile.iloc[:3000, 1].values
            self.graph_num= graph_num
            self.sample_rate= 1/(self.signal_data_time[1]- self.signal_data_time[0])

        elif(self.file_extension=="wav"):
           
            self.sample_rate, signal = wavfile.read(file_path)
            self.signalnoisy=signal
            self.set_signal_file( self.signalnoisy)
            duration = len(signal) / self.sample_rate
            print(f" signal  noisy: {len(self.signalnoisy)}")
            self.signal_data_time =np.array( np.linspace(0, duration, len(signal)))
            try:
                self.signal_data_amplitude= np.array(signal[:, 0])
            except:
                self.signal_data_amplitude= np.array(signal[:])

            
    def set_signal_file(self,signal):
          self.signalnoisy=signal
          print (f"in set call :{len(self.signalnoisy)}")
    def get_signal(self):
        print (f"in get call :{len(self.signalnoisy)}")
        return self.signalnoisy
    def set_signal_graph_num(self, new_graph_num):
        self.graph_num = new_graph_num

    def get_signal_graph_num(self):
        return self.graph_num    

        
