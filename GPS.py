import serial
import pynmea2

def get_gps_data(port="/dev/serial0", baud=9600):
    """
    Scans the serial port for a valid GPS fix.
    Returns a tuple: (latitude, longitude) or (None, None) if no fix.
    """
    try:
        # Initialize the serial connection
        ser = serial.Serial(port, baudrate=baud, timeout=1)
        
        # Loop briefly to catch a fresh GPGGA sentence (contains 3D location)
        for _ in range(20): 
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if line.startswith("$GPGGA"):
                msg = pynmea2.parse(line)
                
                # Check if the sentence actually contains coordinate data
                if msg.latitude and msg.longitude:
                    return msg.latitude, msg.longitude
                    
    except serial.SerialException as e:
        print(f"Serial Port Error: {e}")
    except pynmea2.ParseError as e:
        print(f"NMEA Parsing Error: {e}")
        
    # Return None if the loop finishes without finding valid coordinates
    return None, None

# --- Test Block ---
# This part only runs if you execute this specific file directly.
if __name__ == '__main__':
    print("Attempting to read GPS data...")
    lat, lon = get_gps_data()
    
    if lat and lon:
        print("✅ SUCCESS! GPS Fix Acquired.")
        print(f"Latitude:  {lat}")
        print(f"Longitude: {lon}")
    else:
        print("❌ FAILED. No valid coordinates found.")
        print("Ensure the antenna has a clear view of the sky and the pins are correct.")