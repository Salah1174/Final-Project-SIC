import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2

# Load known face image and encode it
known_face_encodings = []
known_face_names = []

# Load and encode known faces
known_person1_image = face_recognition.load_image_file("/home/rasp/Desktop/Salah.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]

known_person2_image = face_recognition.load_image_file("/home/rasp/Desktop/Seif.jpg")
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]


known_face_encodings.append(known_person1_encoding)
known_face_names.append("Salah")

known_face_encodings.append(known_person2_encoding)
known_face_names.append("Seif")





# Initialize Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    # Capture an image from the camera
    im = picam2.capture_array()

    # Convert the XRGB8888 image to RGB format
    # The XRGB8888 format is a 32-bit image where each pixel is stored as 0xAARRGGBB
    im_rgb = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.uint8)
    im_rgb[:, :, 0] = im[:, :, 1]  # Red channel
    im_rgb[:, :, 1] = im[:, :, 2]  # Green channel
    im_rgb[:, :, 2] = im[:, :, 3]  # Blue channel

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(im_rgb)
    face_encodings = face_recognition.face_encodings(im_rgb, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
        # Draw a rectangle around the face and label it
        cv2.rectangle(im, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(im, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    # Display the image
    cv2.imshow("Camera", im)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the camera and close OpenCV windows
picam2.stop()
cv2.destroyAllWindows()
