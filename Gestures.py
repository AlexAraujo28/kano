import asyncio
from bleak import BleakClient

# Replace with the MAC address and characteristic UUIDs of your Kano Wand
wand_mac_address = "00:00:00:00:00:00"
sensor_data_char_uuid = "0000fff2-0000-1000-8000-00805f9b34fb"  # Example UUID for sensor data

async def connect_and_detect_gestures():
    try:
        print(f"Connecting to Kano Wand with MAC address: {wand_mac_address}")

        async with BleakClient(wand_mac_address) as client:
            await client.connect()

            print("Connected successfully!")

            while True:
                # Read sensor data
                sensor_data = await client.read_gatt_char(sensor_data_char_uuid)

                # Process sensor data and detect gestures
                gesture = detect_gesture(sensor_data)

                if gesture:
                    print(f"Detected gesture: {gesture}")

            await client.disconnect()
            print("Connection closed.")

    except Exception as e:
        print(f"Error: {e}")

def detect_gesture(sensor_data):
    # Replace with actual logic to detect gestures based on sensor_data
    # Example: Using threshold values for accelerometer data to detect basic gestures
    accelerometer_x = sensor_data[0]  # Example: Assuming sensor_data is a list or bytes
    accelerometer_y = sensor_data[1]

    if accelerometer_x > 1000:
        return "right"
    elif accelerometer_x < -1000:
        return "left"
    elif accelerometer_y > 1000:
        return "down"
    elif accelerometer_y < -1000:
        return "up"

    return None  # No gesture detected

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_and_detect_gestures())
