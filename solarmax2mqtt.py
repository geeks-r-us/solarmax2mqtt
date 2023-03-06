import time
import logging
import os

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import paho.mqtt.client as mqtt


# MQTT broker settings
BROKER_IP = os.environ.get('MQTT_BROKER_IP', '127.0.0.1')
BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
TOPIC = os.environ.get('MQTT_TOPIC', 'maxstorage')
CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'solarmax2mqtt')

# Modbus TCP server settings
SERVER_IP = os.environ.get('MODBUS_IP', '127.0.0.1')
SERVER_PORT = int(os.environ.get('MODBUS_PORT','502'))
SLAVE_ID = int(os.environ.get('MODBUS_SLAVE_ID','1'))

# Query delay
QUERY_DELAY = int(os.environ.get('QUERY_DELAY', '10'))

# Loglevel
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN')

# Set up logging
logging.basicConfig(
    level=logging.getLevelName(LOGLEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Connect to Modbus TCP server
client = ModbusTcpClient(SERVER_IP, SERVER_PORT)
client.connect()

# Connect to MQTT broker
mqtt_client = mqtt.Client(client_id=CLIENT_ID)
mqtt_client.connect(BROKER_IP, BROKER_PORT)

# Define the data points you want to read
data_points = [
    {'name': 'SerialNumber', 'address': 100, 'length': 2},
    {'name': 'Firmware', 'address': 102, 'length': 2},
    {'name': 'DC Power MAX.STORAGE', 'address': 110, 'length': 2},
    {'name': 'DC Power PV', 'address': 112, 'length': 2},
    {'name': 'Battery Power', 'address': 114, 'length': 2},
    {'name': 'Self Consumption', 'address': 116, 'length': 2},
    {'name': 'Grid Power', 'address': 118, 'length': 2},
    {'name': 'AC Power', 'address': 120, 'length': 2},
    {'name': 'Battery SoC', 'address': 122, 'length': 1},
]

serial = 0

while True:
    try:
        # Read the values of each data point
        for data_point in data_points:
            # Read the registers for the data point
            result = client.read_input_registers(
                address=data_point['address'],
                count=data_point['length'],
                slave=SLAVE_ID
            )

            # Check if the read was successful
            if result.isError():
                print(f"Modbus error for {data_point['name']}: {result}")
            else:
                # Decode the register values using a binary payload decoder
                decoder = BinaryPayloadDecoder.fromRegisters(
                    result.registers, byteorder=Endian.Big, wordorder=Endian.Little
                )

                # Extract the data point value
                if data_point['length'] == 1:
                    value = decoder.decode_16bit_int()
                elif data_point['length'] == 2:
                    value = decoder.decode_32bit_int()

                # Print the data point value
                logging.info(f"{data_point['name']}: {value}")

                if data_point['name'] == 'SerialNumber':
                    serial = value
                else:
                    # Publish the data to the MQTT broker
                    mqtt_client.publish("{0}/{1}/{2}".format(TOPIC, serial, data_point['name'].replace(' ', '_')) , str(value))

        # Wait for some time before reading again
        time.sleep(QUERY_DELAY)

    except ConnectionError:
        # Handle disconnect by trying to reconnect
        if not client.connected:
            logging.warning("Lost connection to Modbus TCP server. Reconnecting...")
            client.close()
            client.connect()
        
        if not mqtt_client.is_connected():
            logging.warning("Lost connection to MQTT broker. Reconnecting...")
            mqtt_client.reconnect
        