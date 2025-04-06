import easyocr
import gtts
import os
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3

def recognize_text(image_path):
    """ Perform OCR on the given image and return extracted text """
    reader = easyocr.Reader(['en'])
    print("[INFO] Performing OCR on:", image_path)

    result = reader.readtext(image_path)

    if not result:
        print("[ERROR] No text detected!")
        return None  # Stop execution if no text found

    extracted_text = " ".join([res[1] for res in result])
    print("Extracted Text:", extracted_text)
    return extracted_text

def text_to_speech(text, output_file="text_audio.mp3"):
    """ Convert text to speech and play the audio """
    if text:
        tts = gtts.gTTS(text)
        tts.save(output_file)
        play_audio(output_file)

def play_audio(file_path):
    """ Function to play MP3 file using pydub """
    if not os.path.exists(file_path):
        print("[ERROR] Audio file not found!")
        return

    sound = AudioSegment.from_mp3(file_path)
    play(sound)  # Plays the audio without simpleaudio

def text_to_speech_pyttsx3(text):
    """ Alternative text-to-speech using pyttsx3 (Offline) """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    image_path = r"D:\visualapp\image.png"

    if not os.path.exists(image_path):
        print("[ERROR] Image file not found at:", image_path)
    else:
        text = recognize_text(image_path)
        if text:
            print("Reading aloud...")
            text_to_speech_pyttsx3(text)  # Using pyttsx3 for speech output
