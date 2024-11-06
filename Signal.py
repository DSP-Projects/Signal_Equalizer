import pandas as pd

class Signal:
    def __init__(self, graph_num,csv_path ='mmg.csv'):
        self.csv_path = csv_path
        csvFile = pd.read_csv(self.csv_path)   
        self.signal_data_time = csvFile.iloc[:3000, 0].values
        self.signal_data_amplitude = csvFile.iloc[:3000, 1].values
        self.graph_num= graph_num
    
    def set_signal_graph_num(self, new_graph_num):
        self.graph_num = new_graph_num

    def get_signal_graph_num(self):
        return self.graph_num    

        
