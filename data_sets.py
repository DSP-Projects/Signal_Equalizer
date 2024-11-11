import wfdb
import pandas as pd
import os

# Path where your files are located, ensure the trailing slash
data_path = "C:/Users/hagar/ecg_data_sets/"

def convert_to_csv_with_time(record_id):
    # Construct the file path using os.path.join for reliability
    record_path = os.path.join(data_path, record_id)
    
    # Read the record using WFDB
    try:
        record = wfdb.rdrecord(record_path)
    except FileNotFoundError:
        print(f"Error: Could not find the file for record {record_id} at {record_path}")
        return
    
    # Get the sampling frequency (in Hz) from the record metadata
    sampling_frequency = record.fs
    
    # Get the signal data (ECG signal)
    signal_data = record.p_signal
    
    # Select one channel (e.g., the first channel)
    amplitude = signal_data[:, 0]
    
    # Calculate time values based on the sampling frequency
    time = [i / sampling_frequency for i in range(len(amplitude))]
    
    # Create a DataFrame with time and amplitude columns
    df = pd.DataFrame({'Time': time, 'Amplitude': amplitude})
    
    # Save the DataFrame to a CSV file
    output_path = f"{record_id}_time_amplitude.csv"
    df.to_csv(output_path, index=False)
    print(f"Record {record_id} converted to CSV at {output_path}.")

# Example record ID
convert_to_csv_with_time('207')
