import time

from infrared import Infrared # Import your Infrared class

def main():
    print("Initializing Infrared sensor test...")
    ir_sensors = Infrared() # Create an instance of your Infrared class

    print("\n--- Place rover on RUG and note the 'Infrared value' ---")
    print("--- Then place rover on BOX and note the 'Infrared value' ---")
    print("Press Ctrl+C to stop the test.")

    try:
        while True:
            # Read the combined value from all infrared sensors
            current_ir_value = ir_sensors.read_all_infrared()
            # Print the value in both decimal and binary for easy understanding
            print(f"Infrared value: Decimal={current_ir_value}, Binary={bin(current_ir_value)}")
            time.sleep(0.2) # Short delay for continuous reading
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    finally:
        ir_sensors.close() # Ensure GPIO resources are released
        print("Infrared sensor resources released.")

if __name__ == '__main__':
    main()