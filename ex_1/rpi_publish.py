import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 8884
MQTT_TOPIC = "rpi/button"

# -- GPIO Configuration --
BUTTON_PIN = 17 # Use any available GPIO pin

# -- Setup Functions --
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

# -- Main Program --
if __name__ == "__main__":
    setup_gpio()
    
    # Initialize MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print("Press the button to publish 'ON'. Press CTRL+C to exit.")

    try:
        while True:
            button_state = GPIO.input(BUTTON_PIN)
            if button_state == GPIO.LOW: # Button is pressed
                client.publish(MQTT_TOPIC, "ON")
                print(f"Published 'ON' to topic {MQTT_TOPIC}")
                time.sleep(0.5) # Debounce delay
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.loop_stop()
        GPIO.cleanup()