# from azure.iot.device import IoTHubDeviceClient
# import RPi.GPIO as GPIO

# Replace with your device's connection string
CONNECTION_STRING = "Your_Device_Connection_String"

def create_client():
    """
    Creates and returns an Azure IoT Hub client using the provided connection string.
    """
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def listen_for_commands(client):
    """
    Listens for commands from the Azure IoT Hub indefinitely.
    When a command is received, it processes the command.
    """
    while True:
        # Blocking call that waits for a message
        message = client.receive_message()
        print(f"Received message: {message.data}")
        process_command(message.data)

def process_command(command):
    """
    Processes the received command by comparing it to predefined commands.
    Executes the corresponding function to control the valve.
    """
    if command == b'open':
        open_valve()
    elif command == b'close':
        close_valve()
    else:
        print("Unknown command")

# GPIO pin to which the valve is connected
VALVE_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbering
GPIO.setup(VALVE_PIN, GPIO.OUT)  # Set the valve pin as an output

def open_valve():
    """
    Opens the valve by setting the GPIO pin high.
    """
    GPIO.output(VALVE_PIN, GPIO.HIGH)
    print("Valve opened")

def close_valve():
    """
    Closes the valve by setting the GPIO pin low.
    """
    GPIO.output(VALVE_PIN, GPIO.LOW)
    print("Valve closed")

def main():
    """
    Main function to create the client and start listening for commands.
    """
    client = create_client()
    listen_for_commands(client)

if __name__ == "__main__":
    main()
