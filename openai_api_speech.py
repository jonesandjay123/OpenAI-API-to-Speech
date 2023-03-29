import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import speech_recognition as sr
import pyttsx3
import time

# Read API key from file
with open("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()
# Initialize the text to speech engine
engine = pyttsx3.init()

def record_audio(duration, fs=16000):
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return myrecording

def save_wav(filename, audio, fs=16000):
    scipy.io.wavfile.write(filename, fs, audio)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("No question detected.")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    # Speak "Say your question" and start listening immediately after
    speak_text("Say your question")
    
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Adjust these values as needed

    # Save audio to a file
    filename = "input.wav"
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())

    # Transcribe audio to text
    text = transcribe_audio_to_text(filename)
    if text:
        print(f"You said: {text}")

        # Generate the response
        response = generate_response(text)
        print(f"ChatGPT says: {response}")

        # Read response using TTS
        speak_text(response)

try:
    main()
except Exception as e:
    print("An error occurred: {}".format(e))
if __name__ == "__main__":
    main()
