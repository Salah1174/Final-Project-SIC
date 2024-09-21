# 🌾🚜 Smart Farm: Innovative Agriculture for a Sustainable Future 🌞🌱
![Alt text](https://raw.githubusercontent.com/Salah1174/Final-Project-SIC/main/Pictures/Smart%20Farm.png)

## Overview
The **Smart Farm** project is a cutting-edge solution aimed at transforming traditional farming practices using advanced technologies. This system integrates various smart components like facial recognition for security, disease detection in plants, solar panel tracking, smart irrigation, and real-time monitoring via Node-RED 📊🧑‍🌾

---

## Features

### 🔒 Unauthorized Access Detection with Facial Recognition
Security is a top priority. The Smart Farm employs **facial recognition** to detect unauthorized individuals attempting to enter the farm. If any unrecognized face is detected, the system sends alerts to prevent intrusions.
![Alt text](https://github.com/Salah1174/Final-Project-SIC/blob/main/Pictures/FaceDetection.png)

### 🌿 Disease Detection in Plants
The system continuously monitors the health of crops to detect any signs of disease. When an infected plant is found:
- 🌱 It captures the **image** of the infected plant using the Raspberry Pi camera.
- 🧑‍💻 Automatically sends the image to a **Telegram bot** for reporting.
- 📊 The system counts each infected plant, keeping track of occurrences over time.
  ![Alt text](https://github.com/Salah1174/Final-Project-SIC/blob/main/Pictures/IMG-20240714-WA0045.jpg)

### ☀️ Solar Panel Tracking System
The farm is powered by a **solar panel tracking system** that optimizes energy efficiency. The solar panels automatically adjust their angle based on the sun’s position, ensuring maximum energy collection during the day. 
![Alt text](https://github.com/Salah1174/Final-Project-SIC/blob/main/Pictures/Solar%20Panel%20Tracking.jpeg)

### 💧 Smart Irrigation System
Water management is handled by a **smart irrigation system** that ensures plants receive the right amount of water:
- 🌍 Monitors soil moisture levels and weather data in real time.
- 🚰 Automatically irrigates the crops based on the needs of each plant, saving water and resources.

## Smart Water-Level Management System for Efficient Agriculture

The Smart Water-Level Management System is an integral component of a comprehensive smart agriculture solution. Utilizing ultrasonic sensors, this innovative system accurately detects water levels within a tank, ensuring optimal irrigation management. When the tank reaches its maximum capacity, the system automatically halts water intake, preventing overflow and conserving resources. Conversely, it reinitiates water filling when levels drop, promoting efficient water usage. This project exemplifies the integration of technology and agriculture, aiming to enhance sustainability and productivity in farming practices.


### 🌡️ Real-time Monitoring with Node-RED
**Node-RED** is utilized to monitor various sensor data like temperature, humidity, and soil moisture in real-time. This information is visually presented on a **dashboard** that can be accessed remotely:
- 📉 Provides detailed graphs for sensor data.
- ⚠️ Sends alerts for abnormal conditions.
  ![Alt text](https://github.com/Salah1174/Final-Project-SIC/blob/main/Pictures/Smart%20Farm%20(1).png)

### 🤖 Automation via Raspberry Pi
The system’s brain is a **Raspberry Pi** that automates key functions, including:
- Detecting unauthorized access.
- Managing irrigation.
- Monitoring plant health.
- Reporting infections via Telegram.
  ![Alt text](https://github.com/Salah1174/Final-Project-SIC/blob/main/Pictures/Rasperipi.png)
  
---

## Project Highlights
- 🛡️ **Secure**: Protects the farm with advanced facial recognition.
- 🌍 **Eco-Friendly**: Powered by solar energy.
- 🌱 **Efficient**: Automated irrigation and plant health detection.
- 📡 **Smart**: Real-time data monitoring through Node-RED.
- 🤖 **Integrated**: Utilizes Raspberry Pi for seamless automation and communication.

---

## Future Enhancements
- 📶 Implementing IoT-based **remote farm control**.
- 🛰️ Integrating AI for more accurate disease detection and predictive analysis.
- 📷 Enhancing **camera resolution** for higher-quality plant images.

---

Stay tuned for more updates as the **Smart Farm** evolves into an even more powerful tool for modern agriculture! 🚜🌾
