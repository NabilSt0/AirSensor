import serial
import snowflake.connector

# Snowflake connection information
USER = 'ELJAINABIL01'
PASSWORD = 'Nabilox123@'
ACCOUNT = 'py05488.ca-central-1.aws'  
WAREHOUSE = 'MY_SENSOR_DATA_WAREHOUSE'  
DATABASE = 'EnvironmentalData'         
SCHEMA = 'public'

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)

# Prepare the insert query
insert_query = """
    INSERT INTO SensorReadings (ENS160StatusFlag, AirQualityIndex, TVOC_ppb, ECO2_ppm, RelativeHumidity_Percent, Pressure_Pa, Altitude_Meters, Altitude_Feet, Temperature_C, Temperature_F)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Assuming you've connected to Snowflake and set up `insert_query` as before
# Connect to Snowflake and set up your insert_query as previously defined

ser = serial.Serial('COM3', 115200, timeout=1)

# Initially skip the first line assuming it's the header
header_line = ser.readline()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        
        # Skip any header lines that reappear in the data stream
        if "ENS160 Status Flag" in line:
            continue

        data = line.split(',')

        # Ensure data is a list of strings representing numbers before insertion
        try:
            # Convert data to float to ensure it's numeric
            float_data = [float(i) for i in data]
            with conn.cursor() as cur:
                cur.execute(insert_query, float_data)
            print(f"Inserted data to Snowflake: {float_data}")
        except ValueError as ve:
            # Handle the case where conversion to float fails
            print(f"Non-numeric data encountered, skipping insertion: {line}")
        except Exception as e:
            # Handle other exceptions, such as database insertion errors
            print(f"Failed to insert data: {data}, Error: {e}")

except KeyboardInterrupt:
    print("Program terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    ser.close()  # Close the serial port
    conn.close()  # Close the Snowflake connection