import easyocr
import cv2
import pyttsx3

def speak_text(text):
    """Convert text to speech (offline using pyttsx3)"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

def main():
    print("[INFO] Starting webcam for real-time OCR...")
    reader = easyocr.Reader(['en'])  # Load OCR model for English
    cap = cv2.VideoCapture(0)  # Open default webcam

    prev_text = ""  # To avoid repeating the same text

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Show the current frame
        cv2.imshow("Live OCR - Press 'q' to Quit", frame)

        # OCR on the current frame
        results = reader.readtext(frame)
        current_text = " ".join([res[1] for res in results]).strip()

        # Speak text if it's new
        if current_text and current_text != prev_text:
            print("[INFO] Detected Text:", current_text)
            speak_text(current_text)
            prev_text = current_text

        # Quit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
