# delete_sensor_data.py
import snowflake.connector

# Snowflake connection information
USER = 'ELJAINABIL01'
PASSWORD = 'Nabilox123@'
ACCOUNT = 'py05488.ca-central-1.aws'
WAREHOUSE = 'MY_SENSOR_DATA_WAREHOUSE'
DATABASE = 'EnvironmentalData'
SCHEMA = 'public'

def delete_all_records(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM SensorReadings;")
        conn.commit()
        print("All records have been deleted from SensorReadings.")

def main():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )
    
    try:
        confirm = input("Are you sure you want to delete all records from SensorReadings? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_all_records(conn)
        else:
            print("Deletion cancelled.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
