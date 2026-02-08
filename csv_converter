import pandas as pd
import os
import serial
import time
from io import StringIO

PORT = "COM3"
BAUD = 9600


def csv_append(string_block):
    
    input_string = string_block
    ## Test Data: "2026-DDDD 10:00,22.5,45\n2026-02-07 10:05,22.6,44\n2026-02-07 10:10,22.7,43\n2026-02-07 10:15,22.8,42\n2026-02-07 10:20,22.9,41\n2026-02-07 10:25,23.0,40\n2026-02-07 10:30,23.1,39\n2026-02-07 10:35,23.2,38\n2026-02-07 10:40,23.3,37\n2026-02-07 10:45,23.4,36\n2026-02-07 10:50,23.5,35\n2026-02-07 10:55,23.6,34\n2026-02-07 11:00,23.7,33\n2026-02-07 11:05,23.8,32\n2026-02-07 11:10,23.9,31\n2026-02-07 11:15,24.0,30\n2026-02-07 11:20,24.1,29\n2026-02-07 11:25,24.2,28\n2026-02-07 11:30,24.3,27\n2026-02-07 11:35,24.4,26\n"
    ##lines = input_string.strip().split('\n')

    ##records = [line.split(',') for line in lines]

    input_string = string_block.strip()
    
    lines = input_string.split('\n')
    records = [line.split(',') for line in lines if line.strip()]

    df = pd.DataFrame(records, columns=['timestamp', 'temperature', 'humidity'])

    df['temperature'] = pd.to_numeric(df['temperature'])
    df['humidity'] = pd.to_numeric(df['humidity'])

    print(df.head())

    dir_path = Path("data")
    os.makedirs(dir_path, exist_ok=True)
    csv_path = os.path.join(dir_path, 'data.csv')
    
    header = not os.path.exists(csv_path)
    df.to_csv(csv_path, mode='a', header=header, index=False)
    

def listen_to_port(port="COM3", baud=9600, buffer_size=20):
    """Listen to serial port and append data to CSV in batches"""
    
    ser = serial.Serial(port, baud, timeout=1)
    print(f"Connected to {port}. Logging data...")
    
    buffer = []
    
    try:
        while True:
            line = ser.readline().decode("utf-8").strip()
            
            if line:
                print(line)  # Show in console
                buffer.append(line)
                
                if len(buffer) >= buffer_size:
                    string_block = '\n'.join(buffer)
                    csv_append(string_block)
                    buffer = []  # Clear buffer
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        if buffer:
            string_block = '\n'.join(buffer)
            csv_append(string_block)
    finally:
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    listen_to_port(port="COM3", baud=9600, buffer_size=20)

