import cv2
import pyttsx3
import pytesseract
from ultralytics import YOLO

# Set Tesseract-OCR path (Update this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load YOLO model
model = YOLO("yolov8n.pt")  

# Initialize text-to-speech engine
tts = pyttsx3.init()
tts.setProperty("rate", 150)

# Open webcam
cap = cv2.VideoCapture(0)

# Multi-frame detection settings
detected_frames = {}  
required_frames = 5  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame, conf=0.6, iou=0.5, imgsz=640)
    detected_objects = [model.names[int(box.cls)] for box in results[0].boxes] if results[0].boxes else []

    # Track detections across multiple frames
    for obj in detected_objects:
        detected_frames[obj] = detected_frames.get(obj, 0) + 1

    # Process image for text recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Resize
    gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # Apply threshold

    # Extract text using Tesseract
    text = pytesseract.image_to_string(gray, lang="eng").strip()

    # Confirm detected objects & text
    confirmed_objects = [obj for obj, count in detected_frames.items() if count >= required_frames]
    
    if confirmed_objects or text:
        description = "I detected: " + ", ".join(confirmed_objects) if confirmed_objects else ""
        if text:
            description += f" Also, I found some text: {text}"

        print(description)

        # Convert text to speech
        tts.say(description)
        tts.runAndWait()
        break  # Stop after detecting objects or text

    # Display results
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Object & Text Detection", annotated_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
