from picamera2 import Picamera2
from ultralytics import YOLO
import bluetooth
import face_recognition
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import serial
import requests
import re
# import queue
# import threading

# Initialize MQTT
broker_url = "b8c7ac0cf61549cdbf366299ec2d5807.s1.eu.hivemq.cloud"  
broker_port = 8883 
Topic_Logs = "Logs"
Topic_Infection = "Infection"
Topic_Voltage = "Solar_Panel"
Topic_Sound = "Sound_Sensor"
Topic_Moisture = "Soil_Moisture"
Topic_Gas = "Gas_Sensor"
Topic_Temp_DHT = "Temp_Dht"
Topic_Humd_DHT = "Humd_Dht"
Topic_WaterLevel = "Ultrasonic"

client = mqtt.Client()
client.username_pw_set("hivemq.webclient.1726841653034", "VDBSnJl<6%&3f72Fov?d")
client.tls_set()
client.connect(broker_url, broker_port)
# client.loop_forever()

# Initialize GPIO for IR sensor
GPIO.setmode(GPIO.BCM)
IR_PIN = 23
GPIO.setup(IR_PIN, GPIO.IN)

# Initialize PiCamera2 and YOLO
picam2 = Picamera2()
yolo_model = YOLO("best.pt")

# Load known face encodings
known_face_encodings = []
known_face_names = []

# Load and encode known faces
known_person1_image = face_recognition.load_image_file("/home/rasp/Desktop/Salah.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_names.append("Salah")

known_person1_image = face_recognition.load_image_file("/home/rasp/Desktop/Salah2.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_names.append("Salah")

# Initialize Bluetooth for solar tracking data
hc06 = serial.Serial('/dev/rfcomm0',9600,timeout = 1)
hc06.flush()

# Initialize Bluetooth for solar tracking data
hc05 = serial.Serial('/dev/rfcomm0',9600,timeout = 1)
hc05.flush()


# Queue to store solar tracking data from Bluetooth
# voltage_queue = queue.Queue()

# Queue to store solar tracking data from Bluetooth
# waterLevel_ = queue.Queue()

# Counter for detected infections
infection_count = 0

# Telegram bot parameters
TOKEN = "7290187905:AAHp7vnjffhKLlAW23e0Z7IoEQ37tEPf_SE"  # Replace with your bot token
CHAT_IDS = ['955629733', '1204758459']  # List of chat IDs (can be group or individual chat IDs)
message_count = 0  # Counter for the number of detections

# Function to send message and image to Telegram groups or multiple people
def send_telegram_message(count, message, image_path=None):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        r = requests.get(url)
        # print(f"Message to {chat_id}: ", r.json())

        if image_path:
            files = {'photo': open(image_path, 'rb')}
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
            r = requests.post(url, files=files)
            # print(f"Image to {chat_id}: ", r.json())

# def handle_bluetooth():
#     while True:
#         try:
#             if hc05.in_waiting > 0:
#                 data = hc05.readline().decode('utf-8').rstrip()
#                 # print(f"Received Bluetooth data: {data}")
                
#                 # Extract Deep value
#                 if "Deep" in data:
#                     deep_value = data.split("Deep : ")[1].split(",")[0]  # Extract the Deep value
#                     # print(f"Extracted Deep: {deep_value}")
#                     # client.publish(Topic_Humd_DHT, f"{deep_value}", qos=1)
#                     # Optionally, put the deep value in the queue
#                     waterLevel_queue.put(deep_value)
                
#                 # Extract Voltage value
#                 if "Voltage" in data:
#                     voltage_value = data.split("Voltage: ")[1].split(",")[0]  # Extract the Voltage value
#                     # print(f"Extracted Voltage: {voltage_value}")
#                     # client.publish(Topic_Voltage, f"{voltage_value}", qos=1)

#                     # Optionally, put the voltage value in the queue
#                     voltage_queue.put(voltage_value)
                    
#         except bluetooth.BluetoothError as e:
#             print(f"Bluetooth Error: {e}")
#             break



# def publish_mqtt_solar_data():
#     while not voltage_queue.empty():
#         # Get data from the queue
#         data = voltage_queue.get()
#         client.publish(Topic_Voltage, f"{data}", qos=1)


# def publish_mqtt_waterLevel_data():

#     while not waterLevel_queue.empty():
#         # Get data from the queue
#         data = waterLevel_queue.get()
#         client.publish(Topic_Humd_DHT, f"{data}", qos=1)

def run_face_detection():
    print("Running Face Detection...")
    try:
        while True:
            # Capture an image from the camera
            im = picam2.capture_array()

            # Convert the XRGB8888 image to RGB format
            im_rgb = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.uint8)
            im_rgb[:, :, 0] = im[:, :, 1]  # Red channel
            im_rgb[:, :, 1] = im[:, :, 2]  # Green channel
            im_rgb[:, :, 2] = im[:, :, 3]  # Blue channel

            # Find face locations and encodings
            face_locations = face_recognition.face_locations(im_rgb)
            face_encodings = face_recognition.face_encodings(im_rgb, face_locations)

            face_detected = False  

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    face_detected = True  # Set flag to True when a face is detected
                    # Log face detection to MQTT
                    client.publish(Topic_Logs, f"Face detected: {name}", qos=1)
                elif False in matches:
                    Unknown_image_path = "Unknown.jpg"
                    cv2.imwrite(Unknown_image_path, im_rgb[top:bottom, left:right])  # Corrected slice order
                    # Send message and image to Telegram groups/people
                    send_telegram_message(message_count, "Detected Unknown!", Unknown_image_path)
                    face_detected = True

                # Draw a rectangle around the face and label it
                cv2.rectangle(im, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(im, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Display the image
            cv2.imshow("Face Detection", im)

            # If a known face is detected, exit face detection
            if face_detected:
                print(f"Face detected: {name}. Exiting face detection...")
                break
    
    except KeyboardInterrupt:
        print("Interrupt received. Closing...")
    finally:
        print("Face detection finished.")
        cv2.destroyAllWindows()

def run_object_detection():
    
    global infection_count  # To modify the infection_count variable
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()

    print("Starting Object Detection...")
    try:
        while True:
            
            # Capture a frame from the camera
            frame = picam2.capture_array()

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform detection using YOLO
            results = yolo_model(frame_rgb, show=True, conf=0.3)
            result = results[0]

            # Get bounding boxes, confidence, and class names
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            confidences = np.array(result.boxes.conf.cpu(), dtype="float")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")

            # Draw bounding boxes and labels on the frame
            for bbox, confi, cls in zip(bboxes, confidences, classes):
                (x, y, x2, y2) = bbox
                class_id = int(cls)
                object_name = yolo_model.names[class_id]

                if object_name == "infected": 
                    infection_count += 1
                    client.publish(Topic_Infection, f"Infection detected: {infection_count}", qos=1)
                    infected_plant_image_path = f"infected_{message_count}.jpg"
                    cv2.imwrite(infected_plant_image_path, frame[y:y2, x:x2])
                    # Send message and image to Telegram groups/people
                    send_telegram_message(message_count, f"Detected {object_name}!",infected_plant_image_path)

                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

            try:
                if hc05.in_waiting > 0:
                    data = hc05.readline().decode('utf-8').rstrip()

                    if "Deep" in data:
                        deep_value = data.split("Deep : ")[1].split(",")[0]  
                        client.publish(Topic_WaterLevel, f"{deep_value}", qos=1)
 
                    # Extract Voltage value
                    if "Voltage" in data:
                        voltage_value = data.split("Voltage: ")[1].split(",")[0] 
                        voltage_ = voltage_value
                        client.publish(Topic_Voltage, f"{voltage_}", qos=1)
  
                if hc06.in_waiting > 0:
                    data1 = hc06.readline().decode('utf-8').rstrip()

                    # Use regular expressions to find the values in the data
                    pattern = r"Moisture:\s([\d.]+)%\s\|\sLight Intensity:\s(\d+)\s\|\sTemperature:\s([\d.]+)°C\s\|\sHumidity:\s([\d.]+)%\s\|\sGas Level:\s(\d+)"
                    match = re.search(pattern, data1)

                    if match:
                        moisture = match.group(1)  # Extracted moisture value
                        light_intensity = match.group(2)  # Extracted light intensity value
                        temperature = match.group(3)  # Extracted temperature value
                        humidity = match.group(4)  # Extracted humidity value
                        gas_level = match.group(5)  # Extracted gas level value

                        client.publish(Topic_Humd_DHT, f"{humidity}", qos=1)
                        client.publish(Topic_Temp_DHT, f"{temperature}", qos=1)
                        client.publish(Topic_Gas, f"{gas_level}", qos=1)
                        client.publish(Topic_Moisture, f"{moisture}", qos=1)
                        
            except bluetooth.BluetoothError as e:
                print(f"Bluetooth Error: {e}")
                break

            # Show the processed frame
            cv2.imshow("Object Detection", frame)

            # Publish solar data from Bluetooth
            # publish_mqtt_solar_data()

            # Publish Water Level from Bluetooth
            # publish_mqtt_waterLevel_data()
            
            client.loop(.1)

            # Check if the IR sensor detects an object
            if GPIO.input(IR_PIN) == 0:  # Active low
                print("Object detected by IR sensor! Switching to face detection...")
                picam2.stop()
                cv2.destroyAllWindows()
                picam2.start()
                run_face_detection()

            # Check if the 'q' key is pressed to exit object detection
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupt received. Closing...")
    finally:
        picam2.stop()
        GPIO.cleanup()  # Clean up GPIO
        cv2.destroyAllWindows()

# # Start Bluetooth thread
# bluetooth_thread = threading.Thread(target=handle_bluetooth, daemon=True)
# bluetooth_thread.start()

# Start the object detection loop
while True:
    run_object_detection()
