import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time # <-- เพิ่มการ import time เข้ามา

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
# แก้ Topic ให้ตรงกับตัวส่งสัญญาณ (ปุ่มกด)
MQTT_TOPIC = "rpi/button" 

# -- GPIO Configuration --
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW) # <-- สั่งให้ไฟดับไว้ก่อนตอนเริ่มโปรแกรม

# -- Callback Functions --
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}\n")

# ฟังก์ชัน on_message คือหัวใจสำคัญที่เราจะแก้ไข
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: '{payload}' on topic '{msg.topic}'")

    # ถ้าได้รับข้อความว่า "ON"
    if payload == "ON":
        print("LED ON")
        GPIO.output(LED_PIN, GPIO.HIGH) # 1. สั่งให้ LED ติด
        
        time.sleep(1) # 2. หน่วงเวลา 1 วินาที (ปรับค่าได้ตามชอบ)
        
        print("LED OFF")
        GPIO.output(LED_PIN, GPIO.LOW) # 3. สั่งให้ LED ดับ

# -- Main Program --
if __name__ == "__main__":
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