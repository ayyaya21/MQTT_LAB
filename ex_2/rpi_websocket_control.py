import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "rpi/control"

# -- GPIO Configuration --
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 100)
# เริ่มต้นด้วย Duty Cycle 100% เพื่อให้ไฟ "ดับ" (เพราะ HIGH คือปิด)
pwm.start(100)

# -- Callback Functions --
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload}")
    
    if payload == "ON":
        # ถ้าต้องการ "เปิด" ให้ส่งค่า 0% (LOW)
        print("LED ON (Duty Cycle 0%)")
        pwm.ChangeDutyCycle(0)
        
    elif payload == "OFF":
        # ถ้าต้องการ "ปิด" ให้ส่งค่า 100% (HIGH)
        print("LED OFF (Duty Cycle 100%)")
        pwm.ChangeDutyCycle(100)
        
    elif payload.startswith("BRIGHTNESS:"):
        try:
            # รับค่าความสว่างจากเว็บ (0-100)
            brightness_from_web = int(payload.split(":")[1])
            
            # --- จุดสำคัญ: สลับค่าความสว่าง ---
            # เว็บส่งมา 0 (มืดสุด) -> เราต้องจ่ายไฟ 100% (HIGH = ปิด)
            # เว็บส่งมา 100 (สว่างสุด) -> เราต้องจ่ายไฟ 0% (LOW = เปิด)
            # สูตรคือ: duty_cycle = 100 - ความสว่างที่ได้รับ
            duty_cycle = 100 - brightness_from_web
            
            if 0 <= duty_cycle <= 100:
                print(f"Setting brightness to {brightness_from_web}%, Duty Cycle to {duty_cycle}%")
                pwm.ChangeDutyCycle(duty_cycle)
                
        except (IndexError, ValueError):
            print("Invalid brightness value received.")

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