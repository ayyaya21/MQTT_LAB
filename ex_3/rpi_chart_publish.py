import paho.mqtt.client as mqtt
import time
import random

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "rpi/sensor"

# -- Main Program --
if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    print("Publishing sensor data... Press CTRL+C to exit.")
    
    try:
        while True:
            # Replace with actual sensor reading logic
            # For example, reading from an ADC for a variable resistor
            sensor_value = random.randint(0, 100) 
            
            client.publish(MQTT_TOPIC, sensor_value)
            print(f"Published value: {sensor_value}")
            time.sleep(2) # Publish every 2 seconds
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.disconnect()