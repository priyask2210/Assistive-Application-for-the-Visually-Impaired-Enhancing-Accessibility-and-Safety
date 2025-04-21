import cv2
import torch
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the YOLO model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# Open webcam (or replace with a video file path)
cap = cv2.VideoCapture(0)

# Function to play alert sound
def play_alert():
    pygame.mixer.music.load("alert.mp3")  # Load the MP3 file
    pygame.mixer.music.play()

# Loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to RGB (YOLO expects RGB format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform object detection
    results = model(rgb_frame)

    # Show detected objects on frame
    cv2.imshow("Object Detection", results.render()[0])

    # Play an alert sound if an obstacle (like a person) is detected
    for detection in results.pandas().xyxy[0].iterrows():
        label = detection[1]['name']
        if label in ['person', 'bicycle', 'car']:  # Add any obstacles to detect
            play_alert()  # Play alert sound
            break  # Play only once per frame

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
