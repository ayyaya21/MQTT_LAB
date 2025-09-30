import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "rpi/control"

# -- GPIO Configuration --
LED_PIN = 18 # GPIO pin connected to the LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
pwm = GPIO.PWM(LED_PIN, 100) # (pin, frequency)
pwm.start(0) # Start with 0% duty cycle (LED off)

# -- MQTT Callback Functions --
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload}")
    
    if payload == "ON":
        pwm.ChangeDutyCycle(100) # Full brightness
    elif payload == "OFF":
        pwm.ChangeDutyCycle(0) # Off
    elif payload.startswith("BRIGHTNESS:"):
        try:
            brightness = int(payload.split(":")[1])
            if 0 <= brightness <= 100:
                pwm.ChangeDutyCycle(brightness)
        except (IndexError, ValueError):
            print("Invalid brightness value")

# -- Main Program --
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    print("Listening for websocket messages... Press CTRL+C to exit.")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pwm.stop()
        GPIO.cleanup()