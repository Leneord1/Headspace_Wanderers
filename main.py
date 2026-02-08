import serial
import time
from pathlib import Path

# Change this to match your Arduino's COM port
PORT = "COM3"
BAUD = 9600

# Create data directory if missing
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

csv_file = data_dir / "data.csv"

def main():
    # Open serial connection
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Connected to {PORT}. Logging to {csv_file}")

    # Create CSV file with header if it doesn't exist
    if not csv_file.exists():
        with open(csv_file, "w") as f:
            f.write("timestamp,temperature_c,humidity_percent\n")

    while True:
        line = ser.readline().decode("utf-8").strip()

        if line:
            print(line)  # Show in console
            with open(csv_file, "a") as f:
                f.write(line + "\n")

        time.sleep(0.05)

if __name__ == "__main__":
    main()
