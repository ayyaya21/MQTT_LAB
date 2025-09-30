import paho.mqtt.client as mqtt
import time
import random # Library สำหรับสุ่มตัวเลข

# -- MQTT Configuration --
MQTT_BROKER = "broker.hivemq.com"   # Broker เดียวกับหน้าเว็บ
MQTT_PORT = 1883                    # Port สำหรับ Python
MQTT_TOPIC = "rpi/sensor"           # Topic ต้องตรงกับหน้าเว็บ

# -- Main Program --
if __name__ == "__main__":
    client = mqtt.Client()
    
    # เชื่อมต่อกับ Broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("Connected to MQTT Broker!")
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")
        exit()

    client.loop_start() # เริ่มการทำงานเบื้องหลัง

    print(f"Publishing data to topic '{MQTT_TOPIC}'... Press CTRL+C to stop.")

    try:
        while True:
            # --- ส่วนจำลองการอ่านค่าจากเซ็นเซอร์ ---
            # สุ่มตัวเลขทศนิยมระหว่าง 0 ถึง 100
            sensor_value = round(random.uniform(0, 100), 2)
            # ------------------------------------

            # ส่ง (Publish) ข้อมูลที่ได้ไปยัง Broker
            result = client.publish(MQTT_TOPIC, sensor_value)
            
            # เช็คสถานะการส่ง
            status = result[0]
            if status == 0:
                print(f"Sent value: {sensor_value} -> OK")
            else:
                print(f"Failed to send message to topic {MQTT_TOPIC}")

            time.sleep(2) # หน่วงเวลา 2 วินาที ก่อนส่งค่าถัดไป

    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from broker.")