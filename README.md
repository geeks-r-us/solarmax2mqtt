# Solarmax2MQTT

A Python script for reading data from a Solarmax MAX.Storage Ultimate via Modbus TCP and publishing the data to an MQTT broker.

## Prerequisites

- Python 3
- `pymodbus` Python library
- `paho-mqtt` Python library
- A Solarmax inverter with Modbus TCP enabled
- An MQTT broker

## Usage

1. Clone this repository:

git clone https://github.com/exampleuser/solarmax2mqtt.git
cd solarmax2mqtt

2. Install the required Python libraries:

pip install -r requirements.txt

3. Set at least the required environment variables:

export MQTT_BROKER_IP=<your MQTT broker IP address>
export MQTT_BROKER_PORT=<your MQTT broker port>
export MQTT_TOPIC=<your MQTT topic>
export MQTT_CLIENT_ID=<your MQTT client ID>
export MODBUS_IP=<your Solarmax inverter IP address>
export MODBUS_PORT=<your Solarmax inverter Modbus TCP port>
export MODBUS_SLAVE_ID=<your Solarmax inverter Modbus slave ID>

4. Run the script:

python solarmax2mqtt.py


## Docker

Alternatively, you can run the script in a Docker container:

docker build -t solarmax2mqtt .
docker run --rm -it --env-file .env solarmax2mqtt

Note: The `.env` file should contain the required environment variables.

## Environment Variables

| Variable           | Default Value | Description                                                                                                      |
|--------------------|---------------|------------------------------------------------------------------------------------------------------------------|
| `MQTT_BROKER_IP`    | `127.0.0.1`   | The IP address of the MQTT broker.                                                                               |
| `MQTT_BROKER_PORT`  | `1883`        | The port of the MQTT broker.                                                                                     |
| `MQTT_TOPIC`        | `maxstorage`  | The MQTT topic to publish the data to.                                                                            |
| `MQTT_CLIENT_ID`    | `solarmax2mqtt` | The MQTT client ID.                                                                                             |
| `MODBUS_IP`         | `127.0.0.1`   | The IP address of the Solarmax inverter.                                                                          |
| `MODBUS_PORT`       | `502`         | The Modbus TCP port of the Solarmax inverter.                                                                     |
| `MODBUS_SLAVE_ID`   | `1`           | The Modbus slave ID of the Solarmax inverter.                                                                     |
| `QUERY_DELAY`       | `10`          | The delay between Modbus queries, in seconds.                                                                     |
| `LOGLEVEL`          | `WARN`        | The logging level. Valid values are `DEBUG`, `INFO`, `WARN`, `ERROR`, and `CRITICAL`.                            |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pymodbus](https://github.com/riptideio/pymodbus)
- [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)