import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# -- MQTT Configuration --
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "rpi/led"

# -- GPIO Configuration --
LED_PIN = 18 # Use any available GPIO pin

# -- Setup Functions --
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW) # Initially turn off LED

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    if payload == "ON":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
    elif payload == "OFF":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")

# -- Main Program --
if __name__ == "__main__":
    setup_gpio()
    
    # Initialize MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("Listening for messages... Press CTRL+C to exit.")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()