import cv2
import torch
import pytesseract
import pyttsx3
from ultralytics import YOLO
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load YOLO model for object detection
yolo_model = YOLO("yolov8n.pt")  # Use a trained custom model if available

# Load BLIP for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Initialize text-to-speech
engine = pyttsx3.init()

# Configure Tesseract OCR (Make sure Tesseract is installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Capture image from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = yolo_model(frame)

    # Extract bounding boxes and class names
    objects = []
    for box in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = box.tolist()
        label = results[0].names[int(cls)]
        objects.append(label)

    # Convert to a natural sentence
    if objects:
        scene_description = f"In this scene, I see {', '.join(objects)}."
    else:
        scene_description = "No objects detected."

    # Generate a caption for the scene
    inputs = processor(frame, return_tensors="pt")
    caption = caption_model.generate(**inputs)
    caption_text = processor.decode(caption[0], skip_special_tokens=True)

    # Perform OCR for text recognition
    detected_text = pytesseract.image_to_string(frame).strip()

    # Display results
    cv2.imshow("Camera Feed", frame)
    print("Scene Description:", caption_text)
    print("Detected Text:", detected_text)

    # Speak out results
    engine.say(caption_text)
    if detected_text:
        engine.say(f"The text reads: {detected_text}")

    engine.runAndWait()

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
