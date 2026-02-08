import pandas as pd
import os
import serial
import time
from io import StringIO
from pathlib import Path

PORT = "COM3"
BAUD = 9600


def csv_append(string_block):


    try:
        input_string = string_block.strip()

        lines = input_string.split('\n')
        records = []
        for line in lines:
            if line.strip():
                record = line.split(',')
                records.append(record)


        if len(records) == 0:
            print("No records")
            return

        df = pd.DataFrame(records, columns=['timestamp', 'temperature', 'humidity'])

        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

        print(df.head())

        dir_path = Path("data")
        os.makedirs(dir_path, exist_ok=True)
        csv_path = os.path.join(dir_path, 'data.csv')

        df.to_csv(csv_path, mode='a', header=False, index=False)

    except Exception as e:
        print(f"ERROR in csv_append: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


def listen_to_port(port="COM3", baud=9600):

    print(f"Attempting to connect to {port} at {baud} baud...")

    try:
        ser = serial.Serial(port, baud, timeout=1)
    except Exception as e:
        print(f"Failed to connect to {port}: {e}")
        return

    try:
        while True:
            line = ser.readline().decode("utf-8", errors='ignore').strip()

            if line:
                csv_append(line)

            time.sleep(0.05)


    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        ser.close()
        print("Connection closed")


if __name__ == "__main__":
    listen_to_port(port="COM3", baud=9600)